import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { Link, Route, Switch } from "react-router-dom";
import translate from "../../../../utils/translations/translate";
import { commentsView as CommentsView } from "../CommentsView/index";
import { descriptionView as DescriptionView } from "../DescriptionView/index";
import { evidenceView as EvidenceView } from "../EvidenceView/index";
import { exploitView as ExploitView } from "../ExploitView/index";
import { recordsView as RecordsView } from "../RecordsView/index";
import { severityView as SeverityView } from "../SeverityView/index";
import { trackingView as TrackingView } from "../TrackingView/index";
import style from "./index.css";

interface IContextData { findingId: string; projectName: string; userRole: string; }

/* Hack: get projectName and findingId from url
 * This values shall be retrieved from the redux state once the dashboard migration finishes
 */
const getContextData: (() => IContextData) = (): IContextData => {
  const locationElements: string[] = location.hash.split("/");
  const projectName: string = locationElements[2].toLowerCase();
  const findingId: string = locationElements[3].toLowerCase();
  const userRole: string = (window as Window & { userRole: string }).userRole;

  return { findingId, projectName, userRole };
};

// tslint:disable-next-line:no-any Allows to render containers without specifying values for their redux-supplied props
const reduxProps: any = {};
const renderDescription: (() => JSX.Element) = (): JSX.Element => {
  const { findingId, projectName, userRole } = getContextData();
  mixpanel.track("FindingDescription");

  return <DescriptionView findingId={findingId} projectName={projectName} userRole={userRole} {...reduxProps} />;
};
const renderSeverity: (() => JSX.Element) = (): JSX.Element => {
  const { findingId, userRole } = getContextData();
  mixpanel.track("FindingSeverity");

  return <SeverityView findingId={findingId} canEdit={_.includes(["admin", "analyst"], userRole)} {...reduxProps} />;
};
const renderEvidence: (() => JSX.Element) = (): JSX.Element => {
  const { findingId, userRole } = getContextData();
  mixpanel.track("FindingEvidence");

  return <EvidenceView findingId={findingId} canEdit={_.includes(["admin", "analyst"], userRole)} {...reduxProps} />;
};
const renderExploit: (() => JSX.Element) = (): JSX.Element => {
  const { findingId, userRole } = getContextData();
  mixpanel.track("FindingExploit");

  return <ExploitView findingId={findingId} canEdit={_.includes(["admin", "analyst"], userRole)} {...reduxProps} />;
};
const renderTracking: (() => JSX.Element) = (): JSX.Element => {
  const { findingId, userRole } = getContextData();
  mixpanel.track("FindingTracking");

  return <TrackingView findingId={findingId} hasNewVulnerabilities={true} userRole={userRole} {...reduxProps} />;
};
const renderRecords: (() => JSX.Element) = (): JSX.Element => {
  const { findingId, userRole } = getContextData();
  mixpanel.track("FindingRecords");

  return <RecordsView findingId={findingId} canEdit={_.includes(["admin", "analyst"], userRole)} {...reduxProps} />;
};
const renderComments: (() => JSX.Element) = (): JSX.Element => {
  const { findingId } = getContextData();
  mixpanel.track("FindingComments");

  return <CommentsView type="comment" findingId={findingId} />;
};
const renderObservations: (() => JSX.Element) = (): JSX.Element => {
  const { findingId } = getContextData();
  mixpanel.track("FindingObservations");

  return <CommentsView type="observation" findingId={findingId} />;
};

interface IRouterProps {
  match: {
    params: { [key: string]: string };
  };
}

type IFindingContentProps = IRouterProps & {};

const findingContent: React.SFC<IFindingContentProps> = (props: IFindingContentProps): JSX.Element => {
  const { findingId, projectName } = props.match.params;

  return (
    <React.StrictMode>
      <div className={style.mainContainer}>
        <Row>
          <Col md={12} sm={12}>
            <React.Fragment>
              <ul className={`${style.tabsContainer} pills-tabs`}>
                <li id="infoItem" className={style.tab}>
                  <Link to={`/project/${projectName}/${findingId}/description`} aria-expanded="false">
                    <i className="icon s7-note2" />
                    &nbsp;{translate.t("search_findings.tab_description.tab_title")}
                  </Link>
                </li>
                <li id="cssv2Item" className={style.tab}>
                  <Link to={`/project/${projectName}/${findingId}/severity`} aria-expanded="false">
                    <i className="icon s7-calculator" />
                    &nbsp;{translate.t("search_findings.tab_severity.tab_title")}
                  </Link>
                </li>
                <li id="evidenceItem" className={style.tab}>
                  <Link to={`/project/${projectName}/${findingId}/evidence`}>
                    <i className="icon s7-photo" />
                    &nbsp;{translate.t("search_findings.tab_evidence.tab_title")}
                  </Link>
                </li>
                <li id="exploitItem" className={style.tab}>
                  <Link to={`/project/${projectName}/${findingId}/exploit`}>
                    <i className="icon s7-file" />
                    &nbsp;{translate.t("search_findings.tab_exploit.tab_title")}
                  </Link>
                </li>
                <li id="trackingItem" className={style.tab}>
                  <Link to={`/project/${projectName}/${findingId}/tracking`} aria-expanded="true">
                    <i className="icon s7-graph1" />
                    &nbsp;{translate.t("search_findings.tab_tracking.tab_title")}
                  </Link>
                </li>
                <li id="recordsItem" className={style.tab}>
                  <Link to={`/project/${projectName}/${findingId}/records`} aria-expanded="true">
                    <i className="icon s7-notebook" />
                    &nbsp;{translate.t("search_findings.tab_records.tab_title")}
                  </Link>
                </li>
                <li id="commentItem" className={style.tab}>
                  <Link to={`/project/${projectName}/${findingId}/comments`}>
                    <i className="icon s7-comment" />
                    &nbsp;{translate.t("search_findings.tab_comments.tab_title")}
                  </Link>
                </li>
                {/*tslint:disable-next-line:jsx-no-multiline-js Necessary for allowing conditional rendering here*/}
                {_.includes(["admin", "analyst"], (window as Window & { userRole: string }).userRole) ?
                  <li id="observationsItem" className={style.tab}>
                    <Link to={`/project/${projectName}/${findingId}/observations`}>
                      <i className="icon s7-note" />
                      &nbsp;{translate.t("search_findings.tab_observations.tab_title")}
                    </Link>
                  </li>
                  : undefined}
              </ul>

              <div className={style.tabContent}>
                <Switch>
                  <Route path="/project/:projectName/:findingId(\d+)/description" render={renderDescription} />
                  <Route path="/project/:projectName/:findingId(\d+)/severity" render={renderSeverity} />
                  <Route path="/project/:projectName/:findingId(\d+)/evidence" render={renderEvidence} />
                  <Route path="/project/:projectName/:findingId(\d+)/exploit" render={renderExploit} />
                  <Route path="/project/:projectName/:findingId(\d+)/tracking" render={renderTracking} />
                  <Route path="/project/:projectName/:findingId(\d+)/records" render={renderRecords} />
                  <Route path="/project/:projectName/:findingId(\d+)/comments" render={renderComments} />
                  <Route path="/project/:projectName/:findingId(\d+)/observations" render={renderObservations} />
                </Switch>
              </div>
            </React.Fragment>
          </Col>
        </Row>
      </div>
    </React.StrictMode>
  );
};

export { findingContent as FindingContent };
