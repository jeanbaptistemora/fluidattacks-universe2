import { useQuery } from "@apollo/react-hooks";
import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { NavLink, Redirect, Route, RouteComponentProps, Switch } from "react-router-dom";
import { default as globalStyle } from "../../../../styles/global.css";
import translate from "../../../../utils/translations/translate";
import { ProjectIndicatorsView } from "../IndicatorsView/index";
import { ProjectCommentsView } from "../ProjectCommentsView/index";
import { ProjectDraftsView } from "../ProjectDraftsView";
import { ProjectEventsView } from "../ProjectEventsView/index";
import { ProjectFindingsView } from "../ProjectFindingsView/index";
import { ProjectForcesView } from "../ProjectForcesView";
import { ProjectSettingsView } from "../ProjectSettingsView/index";
import { ProjectUsersView } from "../ProjectUsersView/index";
import { GET_ROLE } from "./queries";

type IProjectContentProps = RouteComponentProps<{ projectName: string }>;

const projectContent: React.FC<IProjectContentProps> = (props: IProjectContentProps): JSX.Element => {
  const { projectName } = props.match.params;

  const { data } = useQuery<{ me: { role: string } }>(GET_ROLE, { variables: { projectName } });
  const userRole: string = _.isUndefined(data) || _.isEmpty(data)
    ? (window as typeof window & Dictionary<string>).userRole
    : data.me.role;

  return (
    <React.StrictMode>
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
                  {/*tslint:disable-next-line:jsx-no-multiline-js Necessary for allowing conditional rendering here*/}
                  {_.includes(["admin", "analyst"], userRole) ?
                    <li id="draftsTab" className={globalStyle.tab}>
                      <NavLink activeClassName={globalStyle.active} to={`${props.match.url}/drafts`}>
                        <i className="icon pe-7s-stopwatch" />
                        &nbsp;{translate.t("project.tabs.drafts")}
                      </NavLink>
                    </li>
                    : undefined}
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
                  {/*tslint:disable-next-line:jsx-no-multiline-js Necessary for allowing conditional rendering here*/}
                  {_.includes(["admin", "customeradmin"], userRole) ?
                    <li id="usersTab" className={globalStyle.tab}>
                      <NavLink activeClassName={globalStyle.active} to={`${props.match.url}/users`}>
                        <i className="icon pe-7s-users" />
                        &nbsp;{translate.t("project.tabs.users")}
                      </NavLink>
                    </li>
                    : undefined}
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
    </React.StrictMode>
  );
};

export { projectContent as ProjectContent };
