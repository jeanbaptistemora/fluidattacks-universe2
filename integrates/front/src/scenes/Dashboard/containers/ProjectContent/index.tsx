import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { Redirect, Route, RouteComponentProps, Switch } from "react-router-dom";
import { default as globalStyle } from "../../../../styles/global.css";
import { Can } from "../../../../utils/authz/Can";
import { Have } from "../../../../utils/authz/Have";
import { translate } from "../../../../utils/translations/translate";
import { ContentTab } from "../../components/ContentTab";
import { ChartsForGroupView } from "../ChartsForGroupView";
import { ProjectAuthorsView } from "../ProjectAuthorsView";
import { ProjectCommentsView } from "../ProjectCommentsView/index";
import { ProjectDraftsView } from "../ProjectDraftsView";
import { ProjectEventsView } from "../ProjectEventsView/index";
import { ProjectFindingsView } from "../ProjectFindingsView/index";
import { ProjectForcesView } from "../ProjectForcesView";
import { ProjectSettingsView } from "../ProjectSettingsView/index";
import { ProjectStakeholdersView } from "../ProjectStakeholdersView/index";

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
                    id="analyticsTab"
                    link={`${props.match.url}/analytics`}
                    title={translate.t("group.tabs.analytics.text")}
                    tooltip={translate.t("group.tabs.indicators.tooltip")}
                  />
                  <ContentTab
                    icon="icon pe-7s-light"
                    id="findingsTab"
                    link={`${props.match.url}/vulns`}
                    title={translate.t("group.tabs.findings.text")}
                    tooltip={translate.t("group.tabs.findings.tooltip")}
                  />
                  <Can do="backend_api_resolvers_project__get_drafts">
                    <ContentTab
                      icon="icon pe-7s-stopwatch"
                      id="draftsTab"
                      link={`${props.match.url}/drafts`}
                      title={translate.t("group.tabs.drafts.text")}
                      tooltip={translate.t("group.tabs.drafts.tooltip")}
                    />
                  </Can>
                  <ContentTab
                    icon="icon pe-7s-light"
                    id="forcesTab"
                    link={`${props.match.url}/devsecops`}
                    title={translate.t("group.tabs.forces.text")}
                    tooltip={translate.t("group.tabs.forces.tooltip")}
                  />
                  <ContentTab
                    icon="icon pe-7s-star"
                    id="eventsTab"
                    link={`${props.match.url}/events`}
                    title={translate.t("group.tabs.events.text")}
                    tooltip={translate.t("group.tabs.events.tooltip")}
                  />
                  <ContentTab
                    icon="icon pe-7s-comment"
                    id="commentsTab"
                    link={`${props.match.url}/consulting`}
                    title={translate.t("group.tabs.comments.text")}
                    tooltip={translate.t("group.tabs.comments.tooltip")}
                  />
                  <Can do="backend_api_resolvers_user_resolve_for_group">
                    <ContentTab
                      icon="icon pe-7s-users"
                      id="usersTab"
                      link={`${props.match.url}/stakeholders`}
                      title={translate.t("group.tabs.users.text")}
                      tooltip={translate.t("group.tabs.users.tooltip")}
                    />
                  </Can>
                  <Have I="has_drills_white">
                    <Can do="backend_api_resolvers_project__get_bill">
                      <ContentTab
                        icon="icon pe-7s-users"
                        id="authorsTab"
                        link={`${props.match.url}/authors`}
                        title={translate.t("group.tabs.authors.text")}
                        tooltip={translate.t("group.tabs.authors.tooltip")}
                      />
                    </Can>
                  </Have>
                  <ContentTab
                    icon="icon pe-7s-box1"
                    id="resourcesTab"
                    link={`${props.match.url}/scope`}
                    title={translate.t("group.tabs.resources.text")}
                    tooltip={translate.t("group.tabs.resources.tooltip")}
                  />
                </ul>
              </div>

              <div className={globalStyle.tabContent}>
                <Switch>
                  <Route path={`${props.match.path}/authors`} component={ProjectAuthorsView} exact={true} />
                  <Route path={`${props.match.path}/analytics`} component={ChartsForGroupView} exact={true} />
                  <Route path={`${props.match.path}/vulns`} component={ProjectFindingsView} exact={true} />
                  <Route path={`${props.match.path}/drafts`} component={ProjectDraftsView} exact={true} />
                  <Route path={`${props.match.path}/devsecops`} component={ProjectForcesView} exact={true} />
                  <Route path={`${props.match.path}/events`} component={ProjectEventsView} exact={true} />
                  <Route path={`${props.match.path}/scope`} component={ProjectSettingsView} exact={true} />
                  <Route path={`${props.match.path}/stakeholders`} component={ProjectStakeholdersView} exact={true} />
                  <Route path={`${props.match.path}/consulting`} component={ProjectCommentsView} exact={true} />
                  {/* Necessary to support old resources URLs */}
                  <Redirect path={`${props.match.path}/resources`} to={`${props.match.path}/scope`} />
                  <Redirect to={`${props.match.path}/analytics`} />
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
