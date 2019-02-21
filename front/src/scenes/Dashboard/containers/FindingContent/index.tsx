import React from "react";
import { Col, Row } from "react-bootstrap";
import ReactDOM from "react-dom";
import { BrowserRouter, Link, Route } from "react-router-dom";
import style from "./index.css";

const renderDescription: (() => JSX.Element) = (): JSX.Element => <div />;
const renderSeverity: (() => JSX.Element) = (): JSX.Element => <div />;
const renderEvidence: (() => JSX.Element) = (): JSX.Element => <div />;
const renderExploit: (() => JSX.Element) = (): JSX.Element => <div />;
const renderTracking: (() => JSX.Element) = (): JSX.Element => <div />;
const renderRecords: (() => JSX.Element) = (): JSX.Element => <div />;
const renderComments: (() => JSX.Element) = (): JSX.Element => <div />;
const renderObservations: (() => JSX.Element) = (): JSX.Element => <div />;

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
