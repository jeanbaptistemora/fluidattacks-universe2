import React from "react";
import { Redirect, Route, Switch, useRouteMatch } from "react-router-dom";

import { GroupScopeView } from "../GroupScopeView";
import { GroupToeLinesView } from "../GroupToeLinesView";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { ChartsForGroupView } from "scenes/Dashboard/containers/ChartsForGroupView";
import { ProjectAuthorsView } from "scenes/Dashboard/containers/ProjectAuthorsView";
import { ProjectConsultingView } from "scenes/Dashboard/containers/ProjectConsultingView/index";
import { ProjectDraftsView } from "scenes/Dashboard/containers/ProjectDraftsView";
import { ProjectEventsView } from "scenes/Dashboard/containers/ProjectEventsView/index";
import { ProjectFindingsView } from "scenes/Dashboard/containers/ProjectFindingsView/index";
import { ProjectForcesView } from "scenes/Dashboard/containers/ProjectForcesView";
import { ProjectStakeholdersView } from "scenes/Dashboard/containers/ProjectStakeholdersView/index";
import globalStyle from "styles/global.css";
import {
  Col100,
  Row,
  StickyContainer,
  TabsContainer,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Have } from "utils/authz/Have";
import { useTabTracking } from "utils/hooks";
import { translate } from "utils/translations/translate";

const ProjectContent: React.FC = (): JSX.Element => {
  const { path, url } = useRouteMatch<{ path: string; url: string }>();

  // Side effects
  useTabTracking("Group");

  return (
    <React.StrictMode>
      <div>
        <Row>
          <Col100>
            <React.Fragment>
              <StickyContainer>
                <TabsContainer>
                  <ContentTab
                    icon={"icon pe-7s-graph3"}
                    id={"analyticsTab"}
                    link={`${url}/analytics`}
                    title={translate.t("group.tabs.analytics.text")}
                    tooltip={translate.t("group.tabs.indicators.tooltip")}
                  />
                  <ContentTab
                    icon={"icon pe-7s-light"}
                    id={"findingsTab"}
                    link={`${url}/vulns`}
                    title={translate.t("group.tabs.findings.text")}
                    tooltip={translate.t("group.tabs.findings.tooltip")}
                  />
                  <Can do={"backend_api_resolvers_group_drafts_resolve"}>
                    <ContentTab
                      icon={"icon pe-7s-stopwatch"}
                      id={"draftsTab"}
                      link={`${url}/drafts`}
                      title={translate.t("group.tabs.drafts.text")}
                      tooltip={translate.t("group.tabs.drafts.tooltip")}
                    />
                  </Can>
                  <ContentTab
                    icon={"icon pe-7s-light"}
                    id={"forcesTab"}
                    link={`${url}/devsecops`}
                    title={translate.t("group.tabs.forces.text")}
                    tooltip={translate.t("group.tabs.forces.tooltip")}
                  />
                  <ContentTab
                    icon={"icon pe-7s-star"}
                    id={"eventsTab"}
                    link={`${url}/events`}
                    title={translate.t("group.tabs.events.text")}
                    tooltip={translate.t("group.tabs.events.tooltip")}
                  />
                  <ContentTab
                    icon={"icon pe-7s-comment"}
                    id={"commentsTab"}
                    link={`${url}/consulting`}
                    plus={{ visible: true }}
                    title={translate.t("group.tabs.comments.text")}
                    tooltip={translate.t("group.tabs.comments.tooltip")}
                  />
                  <Can
                    do={
                      "backend_api_resolvers_query_stakeholder__resolve_for_group"
                    }
                  >
                    <ContentTab
                      icon={"icon pe-7s-users"}
                      id={"usersTab"}
                      link={`${url}/stakeholders`}
                      title={translate.t("group.tabs.users.text")}
                      tooltip={translate.t("group.tabs.users.tooltip")}
                    />
                  </Can>
                  <Have I={"has_drills_white"}>
                    <Can do={"backend_api_resolvers_group_bill_resolve"}>
                      <ContentTab
                        icon={"icon pe-7s-users"}
                        id={"authorsTab"}
                        link={`${url}/authors`}
                        title={translate.t("group.tabs.authors.text")}
                        tooltip={translate.t("group.tabs.authors.tooltip")}
                      />
                    </Can>
                  </Have>
                  <Can do={"backend_api_resolvers_git_root_toe_lines_resolve"}>
                    <ContentTab
                      icon={"icon pe-7s-menu"}
                      id={"toeLinesTab"}
                      link={`${url}/toe/lines`}
                      title={translate.t("group.tabs.toeLines.text")}
                      tooltip={translate.t("group.tabs.toeLines.tooltip")}
                    />
                  </Can>
                  <ContentTab
                    icon={"icon pe-7s-box1"}
                    id={"resourcesTab"}
                    link={`${url}/scope`}
                    title={translate.t("group.tabs.resources.text")}
                    tooltip={translate.t("group.tabs.resources.tooltip")}
                  />
                </TabsContainer>
              </StickyContainer>

              <div className={globalStyle.tabContent}>
                <Switch>
                  <Route
                    component={ProjectAuthorsView}
                    exact={true}
                    path={`${path}/authors`}
                  />
                  <Route
                    component={ChartsForGroupView}
                    exact={true}
                    path={`${path}/analytics`}
                  />
                  <Route
                    component={ProjectFindingsView}
                    exact={true}
                    path={`${path}/vulns`}
                  />
                  <Route
                    component={ProjectDraftsView}
                    exact={true}
                    path={`${path}/drafts`}
                  />
                  <Route
                    component={ProjectForcesView}
                    exact={true}
                    path={`${path}/devsecops`}
                  />
                  <Route
                    component={ProjectEventsView}
                    exact={true}
                    path={`${path}/events`}
                  />
                  <Route
                    component={GroupScopeView}
                    exact={true}
                    path={`${path}/scope`}
                  />
                  <Route
                    component={ProjectStakeholdersView}
                    exact={true}
                    path={`${path}/stakeholders`}
                  />
                  <Route
                    component={ProjectConsultingView}
                    exact={true}
                    path={`${path}/consulting`}
                  />
                  <Route
                    component={GroupToeLinesView}
                    exact={true}
                    path={`${path}/toe/lines`}
                  />
                  {/* Necessary to support old resources URLs */}
                  <Redirect path={`${path}/resources`} to={`${path}/scope`} />
                  <Redirect to={`${path}/vulns`} />
                </Switch>
              </div>
            </React.Fragment>
          </Col100>
        </Row>
      </div>
    </React.StrictMode>
  );
};

export { ProjectContent };
