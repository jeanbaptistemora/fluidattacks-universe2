/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Trans } from "react-i18next";
import { Button } from "../../../../components/Button/index";
import { default as globalStyle } from "../../../../styles/global.css";
import { Can } from "../../../../utils/authz/Can";
import translate from "../../../../utils/translations/translate";
import { RemoveProjectModal } from "../../components/RemoveProjectModal";
import { Environments } from "./Environments";
import { Files } from "./Files";
import { Portfolio } from "./Portfolio";
import { Repositories } from "./Repositories";
import { ISettingsViewProps } from "./types";

const projectSettingsView: React.FC<ISettingsViewProps> = (props: ISettingsViewProps): JSX.Element => {
  const { projectName } = props.match.params;
  const { userName, userOrganization } = window as typeof window & Dictionary<string>;

  // Side effects
  const onMount: (() => void) = (): void => {
    mixpanel.track("ProjectResources", { Organization: userOrganization, User: userName });
  };
  React.useEffect(onMount, []);

  // State management
  const [isRemoveModalOpen, setRemoveModalOpen] = React.useState(false);
  const openRemoveModal: (() => void) = (): void => { setRemoveModalOpen(true); };
  const closeRemoveModal: (() => void) = (): void => { setRemoveModalOpen(false); };

  return (
    <React.StrictMode>
      <div id="resources" className="tab-pane cont active">
        <Repositories projectName={props.match.params.projectName} />
        <hr />
        <Environments projectName={props.match.params.projectName} />
        <hr />
        <Files projectName={props.match.params.projectName} />
        <hr />
        <Portfolio projectName={props.match.params.projectName} />
        <Can do="backend_api_resolvers_project__do_request_remove_project">
          <React.Fragment>
            <React.Fragment>
              <hr />
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
                <Col md={4} mdOffset={5}>
                  <ButtonToolbar>
                    <Button onClick={openRemoveModal}>
                      <Glyphicon glyph="minus" />&nbsp;{translate.t("search_findings.tab_resources.removeProject")}
                    </Button>
                  </ButtonToolbar>
                  <RemoveProjectModal
                    isOpen={isRemoveModalOpen}
                    onClose={closeRemoveModal}
                    projectName={projectName.toLowerCase()}
                  />
                </Col>
              </Row>
            </React.Fragment>
          </React.Fragment>
        </Can>
      </div>
    </React.StrictMode>
  );
};

export { projectSettingsView as ProjectSettingsView };
