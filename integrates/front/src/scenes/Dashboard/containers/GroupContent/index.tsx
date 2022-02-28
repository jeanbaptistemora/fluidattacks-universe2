import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";
import { Redirect, Route, Switch, useRouteMatch } from "react-router-dom";

import { groupContext } from "./context";

import { GroupInternalContent } from "../GroupInternalContent";
import { GroupScopeView } from "../GroupScopeView";
import { ToeContent } from "../ToeContent";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { ChartsForGroupView } from "scenes/Dashboard/containers/ChartsForGroupView";
import { GroupAuthorsView } from "scenes/Dashboard/containers/GroupAuthorsView";
import { GroupConsultingView } from "scenes/Dashboard/containers/GroupConsultingView/index";
import { GroupDraftsView } from "scenes/Dashboard/containers/GroupDraftsView";
import { GroupEventsView } from "scenes/Dashboard/containers/GroupEventsView/index";
import { GroupFindingsView } from "scenes/Dashboard/containers/GroupFindingsView/index";
import { GroupForcesView } from "scenes/Dashboard/containers/GroupForcesView";
import { GroupStakeholdersView } from "scenes/Dashboard/containers/GroupStakeholdersView/index";
import { TabContent, TabsContainer } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Have } from "utils/authz/Have";
import { useTabTracking } from "utils/hooks";
import { translate } from "utils/translations/translate";

const GroupContent: React.FC = (): JSX.Element => {
  const { path, url } = useRouteMatch<{ path: string; url: string }>();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canGetToeLines: boolean = permissions.can(
    "api_resolvers_group_toe_lines_resolve"
  );
  const canGetToeInputs: boolean = permissions.can(
    "api_resolvers_group_toe_inputs_resolve"
  );

  // Side effects
  useTabTracking("Group");

  return (
    <React.StrictMode>
      <div>
        <div>
          <div>
            <div>
              <div>
                <TabsContainer>
                  <ContentTab
                    id={"findingsTab"}
                    link={`${url}/vulns`}
                    title={translate.t("group.tabs.findings.text")}
                    tooltip={translate.t("group.tabs.findings.tooltip")}
                  />
                  <ContentTab
                    id={"analyticsTab"}
                    link={`${url}/analytics`}
                    title={translate.t("group.tabs.analytics.text")}
                    tooltip={translate.t("group.tabs.indicators.tooltip")}
                  />
                  <Can do={"api_resolvers_group_drafts_resolve"}>
                    <ContentTab
                      id={"draftsTab"}
                      link={`${url}/drafts`}
                      title={translate.t("group.tabs.drafts.text")}
                      tooltip={translate.t("group.tabs.drafts.tooltip")}
                    />
                  </Can>
                  <ContentTab
                    id={"forcesTab"}
                    link={`${url}/devsecops`}
                    title={translate.t("group.tabs.forces.text")}
                    tooltip={translate.t("group.tabs.forces.tooltip")}
                  />
                  <ContentTab
                    id={"eventsTab"}
                    link={`${url}/events`}
                    title={translate.t("group.tabs.events.text")}
                    tooltip={translate.t("group.tabs.events.tooltip")}
                  />
                  <Have I={"has_squad"}>
                    <Can do={"api_resolvers_group_consulting_resolve"}>
                      <ContentTab
                        id={"commentsTab"}
                        link={`${url}/consulting`}
                        title={translate.t("group.tabs.comments.text")}
                        tooltip={translate.t("group.tabs.comments.tooltip")}
                      />
                    </Can>
                  </Have>
                  <Can
                    do={"api_resolvers_query_stakeholder__resolve_for_group"}
                  >
                    <ContentTab
                      id={"usersTab"}
                      link={`${url}/stakeholders`}
                      title={translate.t("group.tabs.users.text")}
                      tooltip={translate.t("group.tabs.users.tooltip")}
                    />
                  </Can>
                  <Have I={"has_service_white"}>
                    <Can do={"api_resolvers_group_authors_resolve"}>
                      <ContentTab
                        id={"authorsTab"}
                        link={`${url}/authors`}
                        title={translate.t("group.tabs.authors.text")}
                        tooltip={translate.t("group.tabs.authors.tooltip")}
                      />
                    </Can>
                  </Have>
                  {!canGetToeInputs && !canGetToeLines ? undefined : (
                    <ContentTab
                      id={"toeTab"}
                      link={`${url}/surface`}
                      title={translate.t("group.tabs.toe.text")}
                      tooltip={translate.t("group.tabs.toe.tooltip")}
                    />
                  )}
                  <ContentTab
                    id={"resourcesTab"}
                    link={`${url}/scope`}
                    title={translate.t("group.tabs.resources.text")}
                    tooltip={translate.t("group.tabs.resources.tooltip")}
                  />
                </TabsContainer>
              </div>

              <TabContent>
                <groupContext.Provider value={{ path, url }}>
                  <Switch>
                    <Route
                      component={GroupAuthorsView}
                      exact={true}
                      path={`${path}/authors`}
                    />
                    <Route
                      component={ChartsForGroupView}
                      exact={true}
                      path={`${path}/analytics`}
                    />
                    <Route
                      component={GroupFindingsView}
                      exact={true}
                      path={`${path}/vulns`}
                    />
                    <Route
                      component={GroupDraftsView}
                      exact={true}
                      path={`${path}/drafts`}
                    />
                    <Route
                      component={GroupForcesView}
                      exact={true}
                      path={`${path}/devsecops`}
                    />
                    <Route
                      component={GroupEventsView}
                      exact={true}
                      path={`${path}/events`}
                    />
                    <Route
                      component={GroupScopeView}
                      exact={true}
                      path={`${path}/scope`}
                    />
                    <Route
                      component={GroupStakeholdersView}
                      exact={true}
                      path={`${path}/stakeholders`}
                    />
                    <Route
                      component={GroupConsultingView}
                      exact={true}
                      path={`${path}/consulting`}
                    />
                    <Route component={ToeContent} path={`${path}/surface`} />
                    <Route
                      component={GroupInternalContent}
                      path={`${path}/internal`}
                    />
                    <Redirect to={`${path}/vulns`} />
                  </Switch>
                </groupContext.Provider>
              </TabContent>
            </div>
          </div>
        </div>
      </div>
    </React.StrictMode>
  );
};

export { GroupContent };
