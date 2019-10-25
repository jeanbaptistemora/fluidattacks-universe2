import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { NavLink, Redirect, Route, Switch } from "react-router-dom";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import translate from "../../../../utils/translations/translate";
import { IDashboardState } from "../../reducer";
import { ProjectIndicatorsView } from "../IndicatorsView/index";
import { ProjectCommentsView } from "../ProjectCommentsView/index";
import { ProjectDraftsView } from "../ProjectDraftsView";
import { ProjectEventsView } from "../ProjectEventsView/index";
import ProjectFindingsView from "../ProjectFindingsView/index";
import ProjectUsersView from "../ProjectUsersView/index";
import ProjectResourcesView from "../ResourcesView/index";
import { clearProjectState, loadProjectData, ThunkDispatcher } from "./actions";
import style from "./index.css";
import { IProjectContentBaseProps, IProjectContentDispatchProps, IProjectContentProps,
  IProjectContentStateProps } from "./types";

const enhance: InferableComponentEnhancer<{}> = lifecycle<IProjectContentProps, {}>({
  componentDidMount(): void { this.props.onLoad(); },
  componentWillUnmount(): void { this.props.onExit(); },
  componentDidUpdate(previousProps: IProjectContentProps): void {
    const { projectName: currentProject } = this.props.match.params;
    const { projectName: previousProject } = previousProps.match.params;
    if (currentProject !== previousProject) { this.props.onExit(); this.props.onLoad(); }
  },
});

const projectContent: React.FC<IProjectContentProps> = (props: IProjectContentProps): JSX.Element => {
  const { projectName } = props.match.params;

  return (
    <React.StrictMode>
      <div className={style.mainContainer} key={projectName}>
        <Row>
          <Col md={12} sm={12}>
            <React.Fragment>
              <div>
                <ul className={style.tabsContainer}>
                  <li id="indicatorsTab" className={style.tab}>
                    <NavLink activeClassName={style.active} to={`/project/${projectName}/indicators`}>
                      <i className="icon pe-7s-graph3" />
                      &nbsp;{translate.t("project.tabs.indicators")}
                    </NavLink>
                  </li>
                  <li id="findingsTab" className={style.tab}>
                    <NavLink activeClassName={style.active} to={`/project/${projectName}/findings`}>
                      <i className="icon pe-7s-light" />
                      &nbsp;{translate.t("project.tabs.findings")}
                    </NavLink>
                  </li>
                  {/*tslint:disable-next-line:jsx-no-multiline-js Necessary for allowing conditional rendering here*/}
                  {_.includes(["admin", "analyst"], props.userRole) ?
                    <li id="draftsTab" className={style.tab}>
                      <NavLink activeClassName={style.active} to={`/project/${projectName}/drafts`}>
                        <i className="icon pe-7s-stopwatch" />
                        &nbsp;{translate.t("project.tabs.drafts")}
                      </NavLink>
                    </li>
                    : undefined}
                  <li id="eventsTab" className={style.tab}>
                    <NavLink activeClassName={style.active} to={`/project/${projectName}/events`}>
                      <i className="icon pe-7s-star" />
                      &nbsp;{translate.t("project.tabs.events")}
                    </NavLink>
                  </li>
                  <li id="resourcesTab" className={style.tab}>
                    <NavLink activeClassName={style.active} to={`/project/${projectName}/resources`}>
                      <i className="icon pe-7s-box1" />
                      &nbsp;{translate.t("project.tabs.resources")}
                    </NavLink>
                  </li>
                  {/*tslint:disable-next-line:jsx-no-multiline-js Necessary for allowing conditional rendering here*/}
                  {_.includes(["admin", "customeradmin"], props.userRole) ?
                    <li id="usersTab" className={style.tab}>
                      <NavLink activeClassName={style.active} to={`/project/${projectName}/users`}>
                        <i className="icon pe-7s-users" />
                        &nbsp;{translate.t("project.tabs.users")}
                      </NavLink>
                    </li>
                    : undefined}
                  <li id="commentsTab" className={style.tab}>
                    <NavLink activeClassName={style.active} to={`/project/${projectName}/comments`}>
                      <i className="icon pe-7s-comment" />
                      &nbsp;{translate.t("project.tabs.comments")}
                    </NavLink>
                  </li>
                </ul>
              </div>

              <div className={style.tabContent}>
                <Switch>
                  <Route path="/project/:projectName/indicators" component={ProjectIndicatorsView} />
                  <Route path="/project/:projectName/findings" component={ProjectFindingsView} />
                  <Route path="/project/:projectName/drafts" component={ProjectDraftsView} />
                  <Route path="/project/:projectName/events" component={ProjectEventsView} />
                  <Route path="/project/:projectName/resources" component={ProjectResourcesView} />
                  <Route path="/project/:projectName/users" component={ProjectUsersView} />
                  <Route path="/project/:projectName/comments" component={ProjectCommentsView} />
                  <Redirect to="/project/:projectName/indicators" />
                </Switch>
              </div>
            </React.Fragment>
          </Col>
        </Row>
      </div>
    </React.StrictMode>
  );
};

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IProjectContentStateProps, IProjectContentBaseProps, IState> =
  (state: IState): IProjectContentStateProps => ({
    userRole: state.dashboard.user.role,
  });

const mapDispatchToProps: MapDispatchToProps<IProjectContentDispatchProps, IProjectContentBaseProps> =
  (dispatch: ThunkDispatcher, ownProps: IProjectContentBaseProps): IProjectContentDispatchProps => {
    const { projectName } = ownProps.match.params;

    return ({
      onExit: (): void => { dispatch(clearProjectState()); },
      onLoad: (): void => { dispatch(loadProjectData(projectName)); },
    });
  };

export = connect(mapStateToProps, mapDispatchToProps)(enhance(projectContent));
