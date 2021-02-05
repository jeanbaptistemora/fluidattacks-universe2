import _ from "lodash";
import React from "react";
import { Redirect, Route, Switch, useRouteMatch } from "react-router-dom";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { ChartsForGroupView } from "scenes/Dashboard/containers/ChartsForGroupView";
import { ProjectAuthorsView } from "scenes/Dashboard/containers/ProjectAuthorsView";
import { ProjectConsultingView } from "scenes/Dashboard/containers/ProjectConsultingView/index";
import { ProjectDraftsView } from "scenes/Dashboard/containers/ProjectDraftsView";
import { ProjectEventsView } from "scenes/Dashboard/containers/ProjectEventsView/index";
import { ProjectFindingsView } from "scenes/Dashboard/containers/ProjectFindingsView/index";
import { ProjectForcesView } from "scenes/Dashboard/containers/ProjectForcesView";
import { ProjectStakeholdersView } from "scenes/Dashboard/containers/ProjectStakeholdersView/index";
import { default as globalStyle } from "styles/global.css";
import { Col100, Row, StickyContainer, TabsContainer } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Have } from "utils/authz/Have";
import { useTabTracking } from "utils/hooks";
import { translate } from "utils/translations/translate";
import { GroupScopeView } from "../GroupScopeView";

const projectContent: React.FC = (): JSX.Element => {
  const { path, url } = useRouteMatch<{ path: string; url: string }>();

  // Side effects
  useTabTracking("Group");

  return (
    <React.StrictMode>
      <React.Fragment>
        <React.Fragment>
          <Row>
            <Col100>
              <React.Fragment>
                <StickyContainer>
                  <TabsContainer>
                    <ContentTab
                      icon="icon pe-7s-graph3"
                      id="analyticsTab"
                      link={`${url}/analytics`}
                      title={translate.t("group.tabs.analytics.text")}
                      tooltip={translate.t("group.tabs.indicators.tooltip")}
                    />
                    <ContentTab
                      icon="icon pe-7s-light"
                      id="findingsTab"
                      link={`${url}/vulns`}
                      title={translate.t("group.tabs.findings.text")}
                      tooltip={translate.t("group.tabs.findings.tooltip")}
                    />
                    <Can do="backend_api_resolvers_group_drafts_resolve">
                      <ContentTab
                        icon="icon pe-7s-stopwatch"
                        id="draftsTab"
                        link={`${url}/drafts`}
                        title={translate.t("group.tabs.drafts.text")}
                        tooltip={translate.t("group.tabs.drafts.tooltip")}
                      />
                    </Can>
                    <ContentTab
                      icon="icon pe-7s-light"
                      id="forcesTab"
                      link={`${url}/devsecops`}
                      title={translate.t("group.tabs.forces.text")}
                      tooltip={translate.t("group.tabs.forces.tooltip")}
                    />
                    <ContentTab
                      icon="icon pe-7s-star"
                      id="eventsTab"
                      link={`${url}/events`}
                      title={translate.t("group.tabs.events.text")}
                      tooltip={translate.t("group.tabs.events.tooltip")}
                    />
                    <ContentTab
                      icon="icon pe-7s-comment"
                      id="commentsTab"
                      link={`${url}/consulting`}
                      plus={{visible: true}}
                      title={translate.t("group.tabs.comments.text")}
                      tooltip={translate.t("group.tabs.comments.tooltip")}
                    />
                    <Can do="backend_api_resolvers_query_stakeholder__resolve_for_group">
                      <ContentTab
                        icon="icon pe-7s-users"
                        id="usersTab"
                        link={`${url}/stakeholders`}
                        title={translate.t("group.tabs.users.text")}
                        tooltip={translate.t("group.tabs.users.tooltip")}
                      />
                    </Can>
                    <Have I="has_drills_white">
                      <Can do="backend_api_resolvers_group_bill_resolve">
                        <ContentTab
                          icon="icon pe-7s-users"
                          id="authorsTab"
                          link={`${url}/authors`}
                          title={translate.t("group.tabs.authors.text")}
                          tooltip={translate.t("group.tabs.authors.tooltip")}
                        />
                      </Can>
                    </Have>
                    <ContentTab
                      icon="icon pe-7s-box1"
                      id="resourcesTab"
                      link={`${url}/scope`}
                      title={translate.t("group.tabs.resources.text")}
                      tooltip={translate.t("group.tabs.resources.tooltip")}
                    />
                  </TabsContainer>
                </StickyContainer>

                <div className={globalStyle.tabContent}>
                  <Switch>
                    <Route path={`${path}/authors`} component={ProjectAuthorsView} exact={true} />
                    <Route path={`${path}/analytics`} component={ChartsForGroupView} exact={true} />
                    <Route path={`${path}/vulns`} component={ProjectFindingsView} exact={true} />
                    <Route path={`${path}/drafts`} component={ProjectDraftsView} exact={true} />
                    <Route path={`${path}/devsecops`} component={ProjectForcesView} exact={true} />
                    <Route path={`${path}/events`} component={ProjectEventsView} exact={true} />
                    <Route path={`${path}/scope`} component={GroupScopeView} exact={true} />
                    <Route path={`${path}/stakeholders`} component={ProjectStakeholdersView} exact={true} />
                    <Route path={`${path}/consulting`} component={ProjectConsultingView} exact={true} />
                    {/* Necessary to support old resources URLs */}
                    <Redirect path={`${path}/resources`} to={`${path}/scope`} />
                    <Redirect to={`${path}/vulns`} />
                  </Switch>
                </div>
              </React.Fragment>
            </Col100>
          </Row>
        </React.Fragment>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { projectContent as ProjectContent };
