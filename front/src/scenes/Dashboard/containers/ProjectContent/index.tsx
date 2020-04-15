import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { NavLink, Redirect, Route, RouteComponentProps, Switch } from "react-router-dom";
import { default as globalStyle } from "../../../../styles/global.css";
import { Can } from "../../../../utils/authz/Can";
import translate from "../../../../utils/translations/translate";
import { ProjectIndicatorsView } from "../IndicatorsView/index";
import { ProjectCommentsView } from "../ProjectCommentsView/index";
import { ProjectDraftsView } from "../ProjectDraftsView";
import { ProjectEventsView } from "../ProjectEventsView/index";
import { ProjectFindingsView } from "../ProjectFindingsView/index";
import { ProjectForcesView } from "../ProjectForcesView";
import { ProjectSettingsView } from "../ProjectSettingsView/index";
import { ProjectUsersView } from "../ProjectUsersView/index";

type IProjectContentProps = RouteComponentProps<{ projectName: string }>;

const projectContent: React.FC<IProjectContentProps> = (props: IProjectContentProps): JSX.Element => (
  <React.StrictMode>
    <React.Fragment>
      <React.Fragment>
        <Row>
          <Col md={12} sm={12}>
            <React.Fragment>
              <div className={globalStyle.stickyContainer}>
                <ul className={globalStyle.tabsContainer}>
                  <li id="indicatorsTab" className={globalStyle.tab}>
                    <NavLink activeClassName={globalStyle.active} to={`${props.match.url}/indicators`}>
                      <i className="icon pe-7s-graph3" />
                      &nbsp;{translate.t("project.tabs.indicators")}
                    </NavLink>
                  </li>
                  <li id="findingsTab" className={globalStyle.tab}>
                    <NavLink activeClassName={globalStyle.active} to={`${props.match.url}/findings`}>
                      <i className="icon pe-7s-light" />
                      &nbsp;{translate.t("project.tabs.findings")}
                    </NavLink>
                  </li>
                  <Can do="backend_api_resolvers_project__get_drafts">
                    <li id="draftsTab" className={globalStyle.tab}>
                      <NavLink activeClassName={globalStyle.active} to={`${props.match.url}/drafts`}>
                        <i className="icon pe-7s-stopwatch" />
                        &nbsp;{translate.t("project.tabs.drafts")}
                      </NavLink>
                    </li>
                  </Can>
                  <li id="forcesTab" className={globalStyle.tab}>
                    <NavLink activeClassName={globalStyle.active} to={`${props.match.url}/forces`}>
                      <i className="icon pe-7s-light" />
                      &nbsp;{translate.t("project.tabs.forces")}
                    </NavLink>
                  </li>
                  <li id="eventsTab" className={globalStyle.tab}>
                    <NavLink activeClassName={globalStyle.active} to={`${props.match.url}/events`}>
                      <i className="icon pe-7s-star" />
                      &nbsp;{translate.t("project.tabs.events")}
                    </NavLink>
                  </li>
                  <li id="commentsTab" className={globalStyle.tab}>
                    <NavLink activeClassName={globalStyle.active} to={`${props.match.url}/comments`}>
                      <i className="icon pe-7s-comment" />
                      &nbsp;{translate.t("project.tabs.comments")}
                    </NavLink>
                  </li>
                  <Can do="backend_api_resolvers_project__get_users">
                    <li id="usersTab" className={globalStyle.tab}>
                      <NavLink activeClassName={globalStyle.active} to={`${props.match.url}/users`}>
                        <i className="icon pe-7s-users" />
                        &nbsp;{translate.t("project.tabs.users")}
                      </NavLink>
                    </li>
                  </Can>
                  <li id="resourcesTab" className={globalStyle.tab}>
                    <NavLink activeClassName={globalStyle.active} to={`${props.match.url}/resources`}>
                      <i className="icon pe-7s-box1" />
                      &nbsp;{translate.t("project.tabs.resources")}
                    </NavLink>
                  </li>
                </ul>
              </div>

              <div className={globalStyle.tabContent}>
                <Switch>
                  <Route path={`${props.match.path}/indicators`} component={ProjectIndicatorsView} exact={true} />
                  <Route path={`${props.match.path}/findings`} component={ProjectFindingsView} exact={true} />
                  <Route path={`${props.match.path}/drafts`} component={ProjectDraftsView} exact={true} />
                  <Route path={`${props.match.path}/forces`} component={ProjectForcesView} exact={true} />
                  <Route path={`${props.match.path}/events`} component={ProjectEventsView} exact={true} />
                  <Route path={`${props.match.path}/resources`} component={ProjectSettingsView} exact={true} />
                  <Route path={`${props.match.path}/users`} component={ProjectUsersView} exact={true} />
                  <Route path={`${props.match.path}/comments`} component={ProjectCommentsView} exact={true} />
                  <Redirect to={`${props.match.path}/indicators`} />
                </Switch>
              </div>
            </React.Fragment>
          </Col>
        </Row>
      </React.Fragment>
    </React.Fragment>
  </React.StrictMode>
);

export { projectContent as ProjectContent };
