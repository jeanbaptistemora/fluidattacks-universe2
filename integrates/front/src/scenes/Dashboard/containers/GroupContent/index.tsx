import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { GraphQLError } from "graphql";
import React, { useContext } from "react";
import {
  Redirect,
  Route,
  Switch,
  useParams,
  useRouteMatch,
} from "react-router-dom";

import { groupContext } from "./context";

import { GroupInternalContent } from "../GroupInternalContent";
import { GroupScopeView } from "../GroupScopeView";
import { GroupVulnerabilitiesView } from "../GroupVulnerabilitiesView";
import { ToeContent } from "../ToeContent";
import { Alert } from "components/Alert";
import { Dot } from "components/Dot";
import { Tab, Tabs } from "components/Tabs";
import { ChartsForGroupView } from "scenes/Dashboard/containers/ChartsForGroupView";
import { GroupAuthorsView } from "scenes/Dashboard/containers/GroupAuthorsView";
import { GroupConsultingView } from "scenes/Dashboard/containers/GroupConsultingView/index";
import { GET_EVENTS } from "scenes/Dashboard/containers/GroupContent/queries";
import type { IEventsDataset } from "scenes/Dashboard/containers/GroupContent/types";
import { GroupDraftsView } from "scenes/Dashboard/containers/GroupDraftsView";
import { GroupEventsView } from "scenes/Dashboard/containers/GroupEventsView/index";
import { GroupFindingsView } from "scenes/Dashboard/containers/GroupFindingsView/index";
import { GroupForcesView } from "scenes/Dashboard/containers/GroupForcesView";
import { GroupStakeholdersView } from "scenes/Dashboard/containers/GroupStakeholdersView/index";
import { TabContent } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Have } from "utils/authz/Have";
import { featurePreviewContext } from "utils/featurePreview";
import { useTabTracking } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const GroupContent: React.FC = (): JSX.Element => {
  const { path, url } = useRouteMatch<{ path: string; url: string }>();
  const { groupName } = useParams<{ groupName: string }>();
  const { featurePreview } = useContext(featurePreviewContext);

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canGetToeLines: boolean = permissions.can(
    "api_resolvers_group_toe_lines_resolve"
  );
  const canGetToeInputs: boolean = permissions.can(
    "api_resolvers_group_toe_inputs_resolve"
  );
  const { data } = useQuery<IEventsDataset>(GET_EVENTS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.warning("An error occurred loading group data", error);
        msgError(translate.t("groupAlerts.errorTextsad"));
      });
    },
    variables: { groupName },
  });
  const events = data === undefined ? [] : data.group.events;
  const hasOpenEvents =
    events.filter((event): boolean => event.eventStatus === "CREATED").length >
    0;
  const eventFormat: string =
    events.filter((event): boolean => event.eventStatus.includes("CREATED"))
      .length > 0
      ? `${
          events.filter((event): boolean =>
            event.eventStatus.includes("CREATED")
          ).length
        } Event(s) need(s) attention`
      : "None";

  // Side effects
  useTabTracking("Group");

  return (
    <React.StrictMode>
      <div>
        <div>
          <div>
            <div>
              <div>
                <div>
                  {hasOpenEvents ? (
                    <Alert icon={true} variant={"error"}>
                      {eventFormat}
                    </Alert>
                  ) : undefined}
                </div>
                <Tabs>
                  <Tab
                    id={"findingsTab"}
                    link={`${url}/vulns`}
                    tooltip={translate.t("group.tabs.findings.tooltip")}
                  >
                    {translate.t("group.tabs.findings.text")}
                  </Tab>
                  <Tab
                    id={"analyticsTab"}
                    link={`${url}/analytics`}
                    tooltip={translate.t("group.tabs.indicators.tooltip")}
                  >
                    {translate.t("group.tabs.analytics.text")}
                  </Tab>
                  <Can do={"api_resolvers_group_drafts_resolve"}>
                    <Tab
                      id={"draftsTab"}
                      link={`${url}/drafts`}
                      tooltip={translate.t("group.tabs.drafts.tooltip")}
                    >
                      {translate.t("group.tabs.drafts.text")}
                    </Tab>
                  </Can>
                  <Tab
                    id={"forcesTab"}
                    link={`${url}/devsecops`}
                    tooltip={translate.t("group.tabs.forces.tooltip")}
                  >
                    {translate.t("group.tabs.forces.text")}
                  </Tab>
                  <div className={"flex"}>
                    <Tab
                      id={"eventsTab"}
                      link={`${url}/events`}
                      tooltip={translate.t("group.tabs.events.tooltip")}
                    >
                      {translate.t("group.tabs.events.text")}
                      {hasOpenEvents ? <Dot /> : undefined}
                    </Tab>
                  </div>
                  <Have I={"has_squad"}>
                    <Can do={"api_resolvers_group_consulting_resolve"}>
                      <Tab
                        id={"commentsTab"}
                        link={`${url}/consulting`}
                        tooltip={translate.t("group.tabs.comments.tooltip")}
                      >
                        {translate.t("group.tabs.comments.text")}
                      </Tab>
                    </Can>
                  </Have>
                  <Can
                    do={"api_resolvers_query_stakeholder__resolve_for_group"}
                  >
                    <Tab
                      id={"usersTab"}
                      link={`${url}/stakeholders`}
                      tooltip={translate.t("group.tabs.users.tooltip")}
                    >
                      {translate.t("group.tabs.users.text")}
                    </Tab>
                  </Can>
                  <Have I={"has_service_white"}>
                    <Can do={"api_resolvers_group_authors_resolve"}>
                      <Tab
                        id={"authorsTab"}
                        link={`${url}/authors`}
                        tooltip={translate.t("group.tabs.authors.tooltip")}
                      >
                        {translate.t("group.tabs.authors.text")}
                      </Tab>
                    </Can>
                  </Have>
                  {!canGetToeInputs && !canGetToeLines ? undefined : (
                    <Tab
                      id={"toeTab"}
                      link={`${url}/surface`}
                      tooltip={translate.t("group.tabs.toe.tooltip")}
                    >
                      {translate.t("group.tabs.toe.text")}
                    </Tab>
                  )}
                  <Tab
                    id={"resourcesTab"}
                    link={`${url}/scope`}
                    tooltip={translate.t("group.tabs.resources.tooltip")}
                  >
                    {translate.t("group.tabs.resources.text")}
                  </Tab>
                </Tabs>
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
                      component={
                        featurePreview
                          ? GroupVulnerabilitiesView
                          : GroupFindingsView
                      }
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
