/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of conditional rendering
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import LogRocket from "logrocket";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Trans } from "react-i18next";
import { Redirect, Route, Switch, useHistory, useParams, useRouteMatch } from "react-router-dom";
import { Button } from "../../../../components/Button";
import { Modal } from "../../../../components/Modal";
import { authzGroupContext, authzPermissionsContext } from "../../../../utils/authz/config";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { AlertBox } from "../../components/AlertBox";
import { GET_USER_PERMISSIONS } from "../../queries";
import { EventContent } from "../EventContent";
import { FindingContent } from "../FindingContent";
import { ProjectContent } from "../ProjectContent";
import { default as style } from "./index.css";
import {
  GET_GROUP_DATA,
  REJECT_REMOVE_PROJECT_MUTATION,
} from "./queries";
import { IProjectData, IProjectRoute, IRejectRemoveProject } from "./types";

const projectRoute: React.FC<IProjectRoute> = (props: IProjectRoute): JSX.Element => {
  const { setUserRole } = props;
  const { push } = useHistory();
  const { projectName } = useParams<{ projectName: string }>();
  const { path } = useRouteMatch();
  const { userOrganization } = window as typeof window & Dictionary<string>;

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
        LogRocket.captureMessage("Empty permissions", {
          extra: { permissions: JSON.stringify(permData.me.permissions) },
          tags: { level: "group" },
        });
      }
      setUserRole(permData.me.role);
    },
    onError: (permissionsError: ApolloError): void => {
      rollbar.critical(
        "Couldn't load group-level permissions",
        { ...permissionsError },
      );
    },
    variables: { projectName },
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
        rollbar.error("An error occurred group data", groupError);
      });
    },
    variables: { projectName, organization: userOrganization },
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
        rollbar.error("An error occurred rejecting project deletion", rejectError);
      });
    },
  });

  const handleSubmit: (() => void) = (): void => {
    rejectRemoveProject({ variables: { projectName: projectName.toLowerCase() } })
      .catch();
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
            footer={<div />}
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
              <Button bsStyle="default" onClick={closeRejectProjectModal}>
                {translate.t("update_access_token.close")}
              </Button>
              <Button bsStyle="success" disabled={submitting} onClick={handleSubmit}>
                {translate.t("search_findings.tab_indicators.cancelDeletion")}
              </Button>
            </ButtonToolbar>
          </Modal>
        </Row>
      ) :
        <React.Fragment>
          {data.alert.status === 1 ? <AlertBox message={data.alert.message} /> : undefined}
          <Switch>
            <Route path={`${path}/events/:eventId(\\d+)`} component={EventContent} />
            <Route path={`${path}/:type(findings|drafts)/:findingId(\\d+)`} component={FindingContent} />
            {/* Necessary to support legacy URLs before finding had its own path */}
            <Redirect path={`${path}/:findingId(\\d+)`} to={`${path}/findings/:findingId(\\d+)`} />
            <Route path={path} component={ProjectContent} />
          </Switch>
        </React.Fragment>
      }
    </React.StrictMode>
  );
};

export { projectRoute as ProjectRoute };
