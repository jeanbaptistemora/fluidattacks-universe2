/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of conditional rendering
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Trans } from "react-i18next";
import { Redirect, Route, Switch, useHistory, useParams, useRouteMatch } from "react-router-dom";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { EventContent } from "scenes/Dashboard/containers/EventContent";
import { FindingContent } from "scenes/Dashboard/containers/FindingContent";
import { ProjectContent } from "scenes/Dashboard/containers/ProjectContent";
import { default as style } from "scenes/Dashboard/containers/ProjectRoute/index.css";
import {
  GET_GROUP_DATA,
  REJECT_REMOVE_PROJECT_MUTATION,
} from "scenes/Dashboard/containers/ProjectRoute/queries";
import { IProjectData, IProjectRoute, IRejectRemoveProject } from "scenes/Dashboard/containers/ProjectRoute/types";
import { GET_USER_PERMISSIONS } from "scenes/Dashboard/queries";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const projectRoute: React.FC<IProjectRoute> = (props: IProjectRoute): JSX.Element => {
  const { setUserRole } = props;
  const { push } = useHistory();
  const { projectName } = useParams<{ projectName: string }>();
  const { path } = useRouteMatch();

  const closeRejectProjectModal: (() => void) = (): void => {
    push("/home");
  };

  const attributes: PureAbility<string> = React.useContext(authzGroupContext);
  const permissions: PureAbility<string> = React.useContext(authzPermissionsContext);

  // Side effects
  const onProjectChange: (() => void) = (): void => {
    attributes.update([]);
    permissions.update([]);
  };
  React.useEffect(onProjectChange, [projectName]);

  // GraphQL operations
  useQuery(GET_USER_PERMISSIONS, {
    onCompleted: (permData: { me: { permissions: string[]; role: string | undefined } }): void => {
      permissions.update(permData.me.permissions.map((action: string) => ({ action })));
      if (permData.me.permissions.length === 0) {
        Logger.error("Empty permissions", JSON.stringify(permData.me.permissions));
      }
      setUserRole(permData.me.role);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((permissionsError: GraphQLError) => {
        Logger.error(
          "Couldn't load group-level permissions",
          permissionsError,
        );
      });
    },
    variables: {
      entity: "PROJECT",
      identifier: projectName.toLowerCase() },
  });

  const { data, error } = useQuery<IProjectData>(GET_GROUP_DATA, {
    onCompleted: ({ project }: IProjectData) => {
      attributes.update(project.serviceAttributes.map((attribute: string) => ({
        action: attribute,
      })));
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((groupError: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred group data", groupError);
      });
    },
    variables: { projectName },
  });
  const [rejectRemoveProject, { loading: submitting }] = useMutation(
    REJECT_REMOVE_PROJECT_MUTATION, {
    onCompleted: (result: IRejectRemoveProject): void => {
      if (result.rejectRemoveProject.success) {
        closeRejectProjectModal();
        msgSuccess(
          translate.t("search_findings.tab_indicators.success"),
          translate.t("home.newGroup.titleSuccess"),
        );
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      closeRejectProjectModal();
      graphQLErrors.forEach((rejectError: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred rejecting project deletion", rejectError);
      });
    },
  });

  const handleSubmit: (() => void) = (): void => {
    void rejectRemoveProject({ variables: { projectName: projectName.toLowerCase() } });
  };
  if (!_.isUndefined(error)) {
    return (
      <Row>
        <div className={style.noData}>
          <Glyphicon glyph="list" />
        </div>
      </Row>
    );
  }
  if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

  return (
    <React.StrictMode>
      {!_.isEmpty(data.project.deletionDate) ? (
        <Row>
          <div className={style.noData}>
            <Glyphicon glyph="list" />
            <p>{translate.t("route.pendingToDelete")}</p>
          </div>
          <Modal
            headerTitle={translate.t("search_findings.tab_indicators.cancelGroupDeletion")}
            open={true}
          >
            <Row>
              <Col md={12}>
                <Trans>
                  <p>
                    {translate.t(
                      "search_findings.tab_indicators.groupIsRemoving",
                      { deletionDate: data.project.deletionDate, userEmail: data.project.userDeletion })}
                  </p>
                </Trans>
              </Col>
            </Row>
            <br />
            <ButtonToolbar className="pull-right">
              <Button onClick={closeRejectProjectModal}>
                {translate.t("update_access_token.close")}
              </Button>
              <Button disabled={submitting} onClick={handleSubmit}>
                {translate.t("search_findings.tab_indicators.cancelDeletion")}
              </Button>
            </ButtonToolbar>
          </Modal>
        </Row>
      ) :
        <React.Fragment>
          <Switch>
            <Route path={`${path}/events/:eventId(\\d+)`} component={EventContent} />
            <Route path={`${path}/:type(vulns|drafts)/:findingId(\\d+)`} component={FindingContent} />
            {/* Necessary to support legacy URLs before finding had its own path */}
            <Redirect path={`${path}/:findingId(\\d+)`} to={`${path}/vulns/:findingId(\\d+)`} />
            <Route path={path} component={ProjectContent} />
          </Switch>
        </React.Fragment>
      }
    </React.StrictMode>
  );
};

export { projectRoute as ProjectRoute };
