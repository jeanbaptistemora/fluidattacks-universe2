import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { NavLink, Route, RouteComponentProps, Switch } from "react-router-dom";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import translate from "../../../../utils/translations/translate";
import { IDashboardState } from "../../reducer";
import ProjectCommentsView from "../ProjectCommentsView/index";
import ProjectUsersView from "../ProjectUsersView/index";
import ProjectResourcesView from "../ResourcesView/index";
import { loadProjectData, ThunkDispatcher } from "./actions";
import style from "./index.css";

type IProjectContentBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

interface IProjectContentStateProps {
  userRole: string;
}

interface IProjectContentDispatchProps {
  onLoad(): void;
}

type IProjectContentProps = IProjectContentBaseProps & (IProjectContentStateProps & IProjectContentDispatchProps);

const enhance: InferableComponentEnhancer<{}> = lifecycle<IProjectContentProps, {}>({
  componentDidMount(): void { this.props.onLoad(); },
});

const projectContent: React.SFC<IProjectContentProps> = (props: IProjectContentProps): JSX.Element => {
  const { projectName } = props.match.params;

  return (
    <React.StrictMode>
      <div className={style.mainContainer}>
        <Row>
          <Col md={12} sm={12}>
            <React.Fragment>
              <div>
                <ul className={style.tabsContainer}>
                  <li id="indicatorsTab" className={style.tab}>
                    <NavLink activeClassName={style.active} to={`/project/${projectName}/indicators`}>
                      <i className="icon s7-graph3" />
                      &nbsp;{translate.t("project.tabs.indicators")}
                    </NavLink>
                  </li>
                  <li id="findingsTab" className={style.tab}>
                    <NavLink activeClassName={style.active} to={`/project/${projectName}/findings`}>
                      <i className="icon s7-light" />
                      &nbsp;{translate.t("project.tabs.findings")}
                    </NavLink>
                  </li>
                  {/*tslint:disable-next-line:jsx-no-multiline-js Necessary for allowing conditional rendering here*/}
                  {_.includes(["admin", "analyst"], props.userRole) ?
                    <li id="draftsTab" className={style.tab}>
                      <NavLink activeClassName={style.active} to={`/project/${projectName}/drafts`}>
                        <i className="icon s7-stopwatch" />
                        &nbsp;{translate.t("project.tabs.drafts")}
                      </NavLink>
                    </li>
                    : undefined}
                  <li id="eventsTab" className={style.tab}>
                    <NavLink activeClassName={style.active} to={`/project/${projectName}/events`}>
                      <i className="icon s7-star" />
                      &nbsp;{translate.t("project.tabs.events")}
                    </NavLink>
                  </li>
                  <li id="resourcesTab" className={style.tab}>
                    <NavLink activeClassName={style.active} to={`/project/${projectName}/resources`}>
                      <i className="icon s7-box1" />
                      &nbsp;{translate.t("project.tabs.resources")}
                    </NavLink>
                  </li>
                  {/*tslint:disable-next-line:jsx-no-multiline-js Necessary for allowing conditional rendering here*/}
                  {_.includes(["admin", "customeradmin"], props.userRole) ?
                    <li id="usersTab" className={style.tab}>
                      <NavLink activeClassName={style.active} to={`/project/${projectName}/users`}>
                        <i className="icon s7-users" />
                        &nbsp;{translate.t("project.tabs.users")}
                      </NavLink>
                    </li>
                    : undefined}
                  <li id="commentsTab" className={style.tab}>
                    <NavLink activeClassName={style.active} to={`/project/${projectName}/comments`}>
                      <i className="icon s7-comment" />
                      &nbsp;{translate.t("project.tabs.comments")}
                    </NavLink>
                  </li>
                </ul>
              </div>

              <div className={style.tabContent}>
                <Switch>
                  <Route path="/project/:projectName/resources" component={ProjectResourcesView} />
                  <Route path="/project/:projectName/users" component={ProjectUsersView} />
                  <Route path="/project/:projectName/comments" component={ProjectCommentsView} />
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
      onLoad: (): void => { dispatch(loadProjectData(projectName)); },
    });
  };

export = connect(mapStateToProps, mapDispatchToProps)(enhance(projectContent));
