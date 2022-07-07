import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useContext, useMemo } from "react";
import { useTranslation } from "react-i18next";
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
import type {
  IEventBarDataset,
  IEventDataset,
} from "scenes/Dashboard/containers/GroupContent/types";
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

const GroupContent: React.FC = (): JSX.Element => {
  const { path, url } = useRouteMatch<{ path: string; url: string }>();
  const { organizationName } = useParams<{ organizationName: string }>();
  const { featurePreview } = useContext(featurePreviewContext);
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canGetToeLines: boolean = permissions.can(
    "api_resolvers_group_toe_lines_resolve"
  );
  const canGetToeInputs: boolean = permissions.can(
    "api_resolvers_group_toe_inputs_resolve"
  );
  const { data } = useQuery<IEventBarDataset>(GET_EVENTS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.warning("An error occurred loading event bar data", error);
        msgError(t("groupAlerts.errorTextsad"));
      });
    },
    variables: { organizationName },
  });
  const events = useMemo(
    (): IEventDataset[] =>
      data === undefined
        ? []
        : data.organizationId.groups.reduce(
            (previousValue: IEventDataset[], currentValue): IEventDataset[] => [
              ...previousValue,
              ...currentValue.events,
            ],
            []
          ),
    [data]
  );
  const openEvents = events.filter(
    (event): boolean => event.eventStatus === "CREATED"
  );
  const hasOpenEvents = openEvents.length > 0;

  const millisecondsInADay = 86400000;
  const oldestDate = hasOpenEvents
    ? new Date(_.sortBy(openEvents, "eventDate")[0].eventDate)
    : new Date();
  const timeInDays = Math.floor(
    (Date.now() - oldestDate.getTime()) / millisecondsInADay
  );
  const eventMessage: string = t("group.events.eventBar", {
    openEvents: openEvents.length,
    timeInDays,
    vulnGroups: Object.keys(_.countBy(openEvents, "groupName")).length,
  });

  // Side effects
  useTabTracking("Group");

  return (
    <React.StrictMode>
      {hasOpenEvents ? (
        <div className={"mb1"}>
          <Alert icon={true} variant={"error"}>
            {eventMessage}
          </Alert>
        </div>
      ) : undefined}
      <Tabs>
        <Tab
          id={"findingsTab"}
          link={`${url}/vulns`}
          tooltip={t("group.tabs.findings.tooltip")}
        >
          {t("group.tabs.findings.text")}
        </Tab>
        <Tab
          id={"analyticsTab"}
          link={`${url}/analytics`}
          tooltip={t("group.tabs.indicators.tooltip")}
        >
          {t("group.tabs.analytics.text")}
        </Tab>
        <Can do={"api_resolvers_group_drafts_resolve"}>
          <Tab
            id={"draftsTab"}
            link={`${url}/drafts`}
            tooltip={t("group.tabs.drafts.tooltip")}
          >
            {t("group.tabs.drafts.text")}
          </Tab>
        </Can>
        <Tab
          id={"forcesTab"}
          link={`${url}/devsecops`}
          tooltip={t("group.tabs.forces.tooltip")}
        >
          {t("group.tabs.forces.text")}
        </Tab>
        <div className={"flex"}>
          <Tab
            id={"eventsTab"}
            link={`${url}/events`}
            tooltip={t("group.tabs.events.tooltip")}
          >
            {t("group.tabs.events.text")}
            {hasOpenEvents ? <Dot /> : undefined}
          </Tab>
        </div>
        <Have I={"has_squad"}>
          <Can do={"api_resolvers_group_consulting_resolve"}>
            <Tab
              id={"commentsTab"}
              link={`${url}/consulting`}
              tooltip={t("group.tabs.comments.tooltip")}
            >
              {t("group.tabs.comments.text")}
            </Tab>
          </Can>
        </Have>
        <Can do={"api_resolvers_query_stakeholder__resolve_for_group"}>
          <Tab
            id={"usersTab"}
            link={`${url}/stakeholders`}
            tooltip={t("group.tabs.users.tooltip")}
          >
            {t("group.tabs.users.text")}
          </Tab>
        </Can>
        <Have I={"has_service_white"}>
          <Can do={"api_resolvers_group_authors_resolve"}>
            <Tab
              id={"authorsTab"}
              link={`${url}/authors`}
              tooltip={t("group.tabs.authors.tooltip")}
            >
              {t("group.tabs.authors.text")}
            </Tab>
          </Can>
        </Have>
        {!canGetToeInputs && !canGetToeLines ? undefined : (
          <Tab
            id={"toeTab"}
            link={`${url}/surface`}
            tooltip={t("group.tabs.toe.tooltip")}
          >
            {t("group.tabs.toe.text")}
          </Tab>
        )}
        <Tab
          id={"resourcesTab"}
          link={`${url}/scope`}
          tooltip={t("group.tabs.resources.tooltip")}
        >
          {t("group.tabs.resources.text")}
        </Tab>
      </Tabs>
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
                featurePreview ? GroupVulnerabilitiesView : GroupFindingsView
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
            <Route component={GroupInternalContent} path={`${path}/internal`} />
            <Redirect to={`${path}/vulns`} />
          </Switch>
        </groupContext.Provider>
      </TabContent>
    </React.StrictMode>
  );
};

export { GroupContent };
