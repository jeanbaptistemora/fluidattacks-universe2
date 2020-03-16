/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of conditional rendering
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import _ from "lodash";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Trans } from "react-i18next";
import { Redirect, Route, RouteComponentProps, Switch } from "react-router-dom";
import { Button } from "../../../../components/Button";
import { Modal } from "../../../../components/Modal";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { msgSuccess } from "../../../../utils/notifications";
import translate from "../../../../utils/translations/translate";
import { EventContent } from "../EventContent";
import { FindingContent } from "../FindingContent";
import { ProjectContent } from "../ProjectContent";
import { default as style } from "./index.css";
import { GET_PROJECT_DATA, REJECT_REMOVE_PROJECT_MUTATION } from "./queries";
import { IProjectData, IRejectRemoveProject } from "./types";

type PendingRouteProps = RouteComponentProps<{ projectName: string }>;

const pendingRoute: React.FC<PendingRouteProps> = (props: PendingRouteProps): JSX.Element => {
  const { projectName } = props.match.params;
  const [isOpen, setOpen] = React.useState(false);

  const closeRejectProjectModal: (() => void) = (): void => {
    location.assign("/integrates/dashboard#!/home");
  };

  const { data, error } = useQuery(GET_PROJECT_DATA, {
    onCompleted: (projectData: IProjectData): void => {
      if (!_.isEmpty(projectData.project.deletionDate)) { setOpen(true); }
    },
    variables: { projectName },
  });
  const [rejectRemoveProject, {loading: submitting}] = useMutation(REJECT_REMOVE_PROJECT_MUTATION, {
    onCompleted: (result: IRejectRemoveProject): void => {
      if (result.rejectRemoveProject.success) {
        closeRejectProjectModal();
        msgSuccess(
          translate.t("search_findings.tab_indicators.success"),
          translate.t("home.newProject.titleSuccess"),
        );
      }
    },
    onError: (rejectError: ApolloError): void => {
      closeRejectProjectModal();
      handleGraphQLErrors("An error occurred rejecting project deletion", rejectError);
    },
  });

  const handleSubmit: (() => void) = (): void => {
    rejectRemoveProject({ variables: { projectName: projectName.toLowerCase() }})
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
    <React.Fragment>
      {!_.isEmpty(data.project.deletionDate) ?
        <Row>
          <div className={style.noData}>
            <Glyphicon glyph="list" />
            <p>{translate.t("route.pendingToDelete")}</p>
          </div>
          <Modal
            footer={<div />}
            headerTitle={translate.t("search_findings.tab_indicators.cancelProjectDeletion")}
            open={isOpen}
          >
            <Row>
              <Col md={12}>
                <Trans>
                  <p>
                    {translate.t(
                      "search_findings.tab_indicators.projectIsRemoving",
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
              <Button bsStyle="success" type="submit" disabled={submitting} onClick={handleSubmit}>
                {translate.t("search_findings.tab_indicators.cancelDeletion")}
              </Button>
            </ButtonToolbar>
          </Modal>
        </Row>
      :
        <Row>
          <Switch>
            <Route path="/project/:projectName/events/:eventId(\d+)" component={EventContent} />
            <Route
              path="/project/:projectName/:type(findings|drafts)/:findingId(\d+)"
              component={FindingContent}
            />
            <Redirect
              path="/project/:projectName/:findingId(\d+)"
              to="/project/:projectName/findings/:findingId(\d+)"
            />
            <Route path="/project/:projectName" component={ProjectContent} />
          </Switch>
        </Row>}
    </React.Fragment>
  );
};

export { pendingRoute as PendingRoute };
