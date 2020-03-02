/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import { QueryResult } from "@apollo/react-common";
import { Query } from "@apollo/react-components";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Trans } from "react-i18next";
import { Button } from "../../../../components/Button/index";
import { default as globalStyle } from "../../../../styles/global.css";
import translate from "../../../../utils/translations/translate";
import { RemoveProjectModal } from "../../components/RemoveProjectModal";
import { Environments } from "./Environments";
import { Files } from "./Files";
import { Portfolio } from "./Portfolio";
import { GET_PROJECT_DATA } from "./queries";
import { Repositories } from "./Repositories";
import { IGetProjectData, ISettingsViewProps } from "./types";

const renderDeleteBtn: ((props: ISettingsViewProps) => JSX.Element) = (props: ISettingsViewProps): JSX.Element => {
  const projectName: string = props.match.params.projectName;
  const [isProjectModalOpen, setProjectModalOpen] = React.useState(false);
  const openRemoveProjectModal: (() => void) = (): void => {
    setProjectModalOpen(true);
  };
  const closeRemoveProjectModal: (() => void) = (): void => {
    setProjectModalOpen(false);
  };

  return (
    <Query query={GET_PROJECT_DATA} variables={{ projectName }}>
    {
      ({ data }: QueryResult<IGetProjectData>): JSX.Element => {
        if (_.isUndefined(data) || _.isEmpty(data)
        || (!_.isUndefined(data) && !_.isEmpty(data.project.deletionDate))) {
          return <React.Fragment />;
        }
        if (!_.isUndefined(data) && _.isEmpty(data.project.deletionDate)) {
          return (
            <React.Fragment>
              <hr/>
              <Row>
                <Col md={12}>
                  <h3 className={globalStyle.title}>{translate.t("search_findings.tab_resources.removeProject")}</h3>
                </Col>
                <Col md={12}>
                  <Trans>
                    {translate.t("search_findings.tab_resources.warningMessage")}
                  </Trans>
                </Col>
              </Row>
              <Row>
                <br />
                <Col md={2} mdOffset={5}>
                    <ButtonToolbar>
                      <Button onClick={openRemoveProjectModal}>
                        <Glyphicon glyph="minus" />&nbsp;{translate.t("search_findings.tab_resources.removeProject")}
                      </Button>
                    </ButtonToolbar>
                    <RemoveProjectModal
                      isOpen={isProjectModalOpen}
                      onClose={closeRemoveProjectModal}
                      projectName={projectName.toLowerCase()}
                    />
                </Col>
              </Row>
            </React.Fragment>
          );
        } else { return <React.Fragment />; }
      }}
    </Query>

  );
};

const projectSettingsView: React.FC<ISettingsViewProps> = (props: ISettingsViewProps): JSX.Element => {
  const { userName, userOrganization, userRole } = window as typeof window & Dictionary<string>;

  const onMount: (() => void) = (): void => {
    mixpanel.track("ProjectResources", { Organization: userOrganization, User: userName });
  };
  React.useEffect(onMount, []);

  return (
  <React.StrictMode>
    <div id="resources" className="tab-pane cont active">
      <Repositories projectName={props.match.params.projectName} />
      <Environments projectName={props.match.params.projectName} />
      <Files projectName={props.match.params.projectName} />
      <Portfolio projectName={props.match.params.projectName} />
      {_.includes(["admin"], userRole) ? renderDeleteBtn(props) : undefined}
    </div>
  </React.StrictMode>
  );
};

export { projectSettingsView as ProjectSettingsView };
