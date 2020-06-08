import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { Redirect, Route, RouteComponentProps, Switch } from "react-router-dom";
import { default as globalStyle } from "../../../../styles/global.css";
import { Can } from "../../../../utils/authz/Can";
import { Have } from "../../../../utils/authz/Have";
import translate from "../../../../utils/translations/translate";
import { ContentTab } from "../../components/ContentTab";
import { ProjectIndicatorsView } from "../IndicatorsView/index";
import { ProjectAuthorsView } from "../ProjectAuthorsView";
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
                  <ContentTab
                    icon="icon pe-7s-graph3"
                    id="indicatorsTab"
                    link={`${props.match.url}/indicators`}
                    title={translate.t("group.tabs.indicators")}
                  />
                  <ContentTab
                    icon="icon pe-7s-light"
                    id="findingsTab"
                    link={`${props.match.url}/findings`}
                    title={translate.t("group.tabs.findings")}
                  />
                  <Can do="backend_api_resolvers_project__get_drafts">
                    <ContentTab
                      icon="icon pe-7s-stopwatch"
                      id="draftsTab"
                      link={`${props.match.url}/drafts`}
                      title={translate.t("group.tabs.drafts")}
                    />
                  </Can>
                  <ContentTab
                    icon="icon pe-7s-light"
                    id="forcesTab"
                    link={`${props.match.url}/forces`}
                    title={translate.t("group.tabs.forces")}
                  />
                  <ContentTab
                    icon="icon pe-7s-star"
                    id="eventsTab"
                    link={`${props.match.url}/events`}
                    title={translate.t("group.tabs.events")}
                  />
                  <ContentTab
                    icon="icon pe-7s-comment"
                    id="commentsTab"
                    link={`${props.match.url}/comments`}
                    title={translate.t("group.tabs.comments")}
                  />
                  <Can do="backend_api_resolvers_project__get_users">
                    <ContentTab
                      icon="icon pe-7s-users"
                      id="usersTab"
                      link={`${props.match.url}/users`}
                      title={translate.t("group.tabs.users")}
                    />
                  </Can>
                  <Have I="has_drills_white">
                    <Can do="backend_api_resolvers_project__get_bill">
                      <ContentTab
                        icon="icon pe-7s-users"
                        id="authorsTab"
                        link={`${props.match.url}/authors`}
                        title={translate.t("group.tabs.authors")}
                      />
                    </Can>
                  </Have>
                  <ContentTab
                    icon="icon pe-7s-box1"
                    id="resourcesTab"
                    link={`${props.match.url}/settings`}
                    title={translate.t("group.tabs.resources")}
                  />
                </ul>
              </div>

              <div className={globalStyle.tabContent}>
                <Switch>
                  <Route path={`${props.match.path}/authors`} component={ProjectAuthorsView} exact={true} />
                  <Route path={`${props.match.path}/indicators`} component={ProjectIndicatorsView} exact={true} />
                  <Route path={`${props.match.path}/findings`} component={ProjectFindingsView} exact={true} />
                  <Route path={`${props.match.path}/drafts`} component={ProjectDraftsView} exact={true} />
                  <Route path={`${props.match.path}/forces`} component={ProjectForcesView} exact={true} />
                  <Route path={`${props.match.path}/events`} component={ProjectEventsView} exact={true} />
                  <Route path={`${props.match.path}/settings`} component={ProjectSettingsView} exact={true} />
                  <Route path={`${props.match.path}/users`} component={ProjectUsersView} exact={true} />
                  <Route path={`${props.match.path}/comments`} component={ProjectCommentsView} exact={true} />
                  {/* Necessary to support old resources URLs */}
                  <Redirect path={`${props.match.path}/resources`} to={`${props.match.path}/settings`} />
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
