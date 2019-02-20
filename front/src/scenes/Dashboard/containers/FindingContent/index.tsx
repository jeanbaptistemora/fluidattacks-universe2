import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, NavLink, Route } from "react-router-dom";
import style from "./index.css";

const renderDescription: (() => JSX.Element) = (): JSX.Element => <div />;
const renderSeverity: (() => JSX.Element) = (): JSX.Element => <div />;
const renderEvidence: (() => JSX.Element) = (): JSX.Element => <div />;
const renderExploit: (() => JSX.Element) = (): JSX.Element => <div />;
const renderTracking: (() => JSX.Element) = (): JSX.Element => <div />;
const renderRecords: (() => JSX.Element) = (): JSX.Element => <div />;
const renderComments: (() => JSX.Element) = (): JSX.Element => <div />;
const renderObservations: (() => JSX.Element) = (): JSX.Element => <div />;

const findingContent: React.SFC = (): JSX.Element => {
  const locationElements: string[] = location.hash.split("/");
  const projectName: string = locationElements[2].toLowerCase();
  const findingId: string = locationElements[3].toLowerCase();

  return (
    <React.StrictMode>
      <BrowserRouter basename={`dashboard#!/project/${projectName}/${findingId}`}>
        <React.Fragment>
          <ul className={style.tabsContainer}>
            <li className={style.tab}>
              <NavLink to="/description" activeClassName={style.activeTab} aria-expanded="false">
                <i className="icon s7-note2" />&nbsp;Description
              </NavLink>
            </li>
            <li className={style.tab}>
              <NavLink to="/severity" activeClassName={style.activeTab} aria-expanded="false">
                <i className="icon s7-calculator" />&nbsp;Severity
              </NavLink>
            </li>
            <li className={style.tab}>
              <NavLink to="/evidence" activeClassName={style.activeTab}>
                <i className="icon s7-photo" />&nbsp;Evidence
                </NavLink>
            </li>
            <li className={style.tab}>
              <NavLink to="/exploit" activeClassName={style.activeTab}>
                <i className="icon s7-file" />&nbsp;Exploit
              </NavLink>
            </li>
            <li className={style.tab}>
              <NavLink to="/tracking" activeClassName={style.activeTab} aria-expanded="true">
                <i className="icon s7-graph1" />&nbsp;Tracking
              </NavLink>
            </li>
            <li className={style.tab}>
              <NavLink to="/records" activeClassName={style.activeTab} aria-expanded="true">
                <i className="icon s7-notebook" />&nbsp;Records
              </NavLink>
            </li>
            <li className={style.tab}>
              <NavLink to="/comments" activeClassName={style.activeTab}>
                <i className="icon s7-comment" />&nbsp;Comments
              </NavLink>
            </li>
            <li className={style.tab}>
              <NavLink to="/observations" activeClassName={style.activeTab}>
                <i className="icon s7-note" />&nbsp;Observations
              </NavLink>
            </li>
          </ul>

          <Route path="/description" component={renderDescription} />
          <Route path="/severity" component={renderSeverity} />
          <Route path="/evidence" component={renderEvidence} />
          <Route path="/exploit" component={renderExploit} />
          <Route path="/tracking" component={renderTracking} />
          <Route path="/records" component={renderRecords} />
          <Route path="/comments" component={renderComments} />
          <Route path="/observations" component={renderObservations} />
        </React.Fragment>
      </BrowserRouter>
    </React.StrictMode>
  );
};

ReactDOM.render(React.createElement(findingContent), document.getElementById("root"));
