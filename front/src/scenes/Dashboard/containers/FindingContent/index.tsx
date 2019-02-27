import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, Row } from "react-bootstrap";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { BrowserRouter, Link, Route } from "react-router-dom";
import store from "../../../../store/index";
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

const findingContent: React.SFC = (): JSX.Element => (
  <React.StrictMode>
    <div className={style.mainContainer}>
      <Row>
        <Col md={12} sm={12}>
          <BrowserRouter basename={"/integrates/dashboard#!/project"}>
            <React.Fragment>
              <ul className={`${style.tabsContainer} pills-tabs`}>
                <li id="infoItem" className={style.tab}>
                  <Link to="description" aria-expanded="false">
                    <i className="icon s7-note2" />
                    &nbsp;{translate.t("search_findings.tab_description.tab_title")}
                  </Link>
                </li>
                <li id="cssv2Item" className={style.tab}>
                  <Link to="severity" aria-expanded="false">
                    <i className="icon s7-calculator" />
                    &nbsp;{translate.t("search_findings.tab_severity.tab_title")}
                  </Link>
                </li>
                <li id="evidenceItem" className={style.tab}>
                  <Link to="evidence">
                    <i className="icon s7-photo" />
                    &nbsp;{translate.t("search_findings.tab_evidence.tab_title")}
                  </Link>
                </li>
                <li id="exploitItem" className={style.tab}>
                  <Link to="exploit">
                    <i className="icon s7-file" />
                    &nbsp;{translate.t("search_findings.tab_exploit.tab_title")}
                  </Link>
                </li>
                <li id="trackingItem" className={style.tab}>
                  <Link to="tracking" aria-expanded="true">
                    <i className="icon s7-graph1" />
                    &nbsp;{translate.t("search_findings.tab_tracking.tab_title")}
                  </Link>
                </li>
                <li id="recordsItem" className={style.tab}>
                  <Link to="records" aria-expanded="true">
                    <i className="icon s7-notebook" />
                    &nbsp;{translate.t("search_findings.tab_records.tab_title")}
                  </Link>
                </li>
                <li id="commentItem" className={style.tab}>
                  <Link to="comments">
                    <i className="icon s7-comment" />
                    &nbsp;{translate.t("search_findings.tab_comments.tab_title")}
                  </Link>
                </li>
                <li id="observationsItem" className={style.tab}>
                  <Link to="observations">
                    <i className="icon s7-note" />
                    &nbsp;{translate.t("search_findings.tab_observations.tab_title")}
                  </Link>
                </li>
              </ul>

              <Provider store={store}>
              <div className={style.tabContent}>
                <Route path="/:proj/:fin/description" render={renderDescription} />
                <Route path="/:proj/:fin/severity" render={renderSeverity} />
                <Route path="/:proj/:fin/evidence" render={renderEvidence} />
                <Route path="/:proj/:fin/exploit" render={renderExploit} />
                <Route path="/:proj/:fin/tracking" render={renderTracking} />
                <Route path="/:proj/:fin/records" render={renderRecords} />
                <Route path="/:proj/:fin/comments" render={renderComments} />
                <Route path="/:proj/:fin/observations" render={renderObservations} />
              </div>
              </Provider>
            </React.Fragment>
          </BrowserRouter>
        </Col>
      </Row>
    </div>
  </React.StrictMode>
);

mixpanel.init("7a7ceb75ff1eed29f976310933d1cc3e");
ReactDOM.render(React.createElement(findingContent), document.getElementById("root"));
