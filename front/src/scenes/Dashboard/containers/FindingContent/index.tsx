import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import ReactDOM from "react-dom";
import { BrowserRouter, Link, Route } from "react-router-dom";
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

  return <DescriptionView findingId={findingId} projectName={projectName} userRole={userRole} {...reduxProps} />;
};
const renderSeverity: (() => JSX.Element) = (): JSX.Element => {
  const { findingId, userRole } = getContextData();

  return <SeverityView findingId={findingId} canEdit={_.includes(["admin", "analyst"], userRole)} {...reduxProps} />;
};
const renderEvidence: (() => JSX.Element) = (): JSX.Element => {
  const { findingId, userRole } = getContextData();

  return <EvidenceView findingId={findingId} canEdit={_.includes(["admin", "analyst"], userRole)} {...reduxProps} />;
};
const renderExploit: (() => JSX.Element) = (): JSX.Element => {
  const { findingId, userRole } = getContextData();

  return <ExploitView findingId={findingId} canEdit={_.includes(["admin", "analyst"], userRole)} {...reduxProps} />;
};
const renderTracking: (() => JSX.Element) = (): JSX.Element => {
  const { findingId, userRole } = getContextData();

  return <TrackingView findingId={findingId} hasNewVulnerabilities={true} userRole={userRole} {...reduxProps} />;
};
const renderRecords: (() => JSX.Element) = (): JSX.Element => {
  const { findingId, userRole } = getContextData();

  return <RecordsView findingId={findingId} canEdit={_.includes(["admin", "analyst"], userRole)} {...reduxProps} />;
};
const renderComments: (() => JSX.Element) = (): JSX.Element => {
  const { findingId } = getContextData();

  return <CommentsView type="comment" findingId={findingId} />;
};
const renderObservations: (() => JSX.Element) = (): JSX.Element => {
  const { findingId } = getContextData();

  return <CommentsView type="observation" findingId={findingId} />;
};

const findingContent: React.SFC = (): JSX.Element => (
  <React.StrictMode>
    <div className={style.mainContainer}>
      <Row>
        <Col md={12} sm={12}>
          <BrowserRouter basename="/dashboard#!/project">
            <React.Fragment>
              <ul className={`${style.tabsContainer} pills-tabs`}>
                <li id="infoItem" className={style.tab}>
                  <Link to="description" aria-expanded="false">
                    <i className="icon s7-note2" />&nbsp;Description
                    </Link>
                </li>
                <li id="cssv2Item" className={style.tab}>
                  <Link to="severity" aria-expanded="false">
                    <i className="icon s7-calculator" />&nbsp;Severity
                    </Link>
                </li>
                <li id="evidenceItem" className={style.tab}>
                  <Link to="evidence">
                    <i className="icon s7-photo" />&nbsp;Evidence
                    </Link>
                </li>
                <li id="exploitItem" className={style.tab}>
                  <Link to="exploit">
                    <i className="icon s7-file" />&nbsp;Exploit
                    </Link>
                </li>
                <li id="trackingItem" className={style.tab}>
                  <Link to="tracking" aria-expanded="true">
                    <i className="icon s7-graph1" />&nbsp;Tracking
                    </Link>
                </li>
                <li id="recordsItem" className={style.tab}>
                  <Link to="records" aria-expanded="true">
                    <i className="icon s7-notebook" />&nbsp;Records
                    </Link>
                </li>
                <li id="commentItem" className={style.tab}>
                  <Link to="comments">
                    <i className="icon s7-comment" />&nbsp;Comments
                    </Link>
                </li>
                <li id="observationsItem" className={style.tab}>
                  <Link to="observations">
                    <i className="icon s7-note" />&nbsp;Observations
                    </Link>
                </li>
              </ul>

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
            </React.Fragment>
          </BrowserRouter>
        </Col>
      </Row>
    </div>
  </React.StrictMode>
);

ReactDOM.render(React.createElement(findingContent), document.getElementById("root"));
