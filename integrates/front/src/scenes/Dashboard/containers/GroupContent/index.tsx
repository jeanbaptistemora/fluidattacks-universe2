/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, {
  Fragment,
  StrictMode,
  useCallback,
  useContext,
  useMemo,
  useState,
} from "react";
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
import type {
  IGetOrganizationId,
  IOrganizationPermission,
} from "../OrganizationContent/types";
import { ToeContent } from "../ToeContent";
import { Button } from "components/Button";
import { Card } from "components/Card";
import { Dot } from "components/Dot";
import { Lottie } from "components/Icon";
import { useShow } from "components/Modal";
import { Tab, Tabs } from "components/Tabs";
import { Text } from "components/Text";
import { lotCircleXMark } from "resources";
import { EventBar } from "scenes/Dashboard/components/EventBar";
import { HelpModal } from "scenes/Dashboard/components/Navbar/HelpModal";
import { ChartsForGroupView } from "scenes/Dashboard/containers/ChartsForGroupView";
import { GroupAuthorsView } from "scenes/Dashboard/containers/GroupAuthorsView";
import { GroupConsultingView } from "scenes/Dashboard/containers/GroupConsultingView/index";
import { GET_GROUP_EVENT_STATUS } from "scenes/Dashboard/containers/GroupContent/queries";
import type { IGetEventStatus } from "scenes/Dashboard/containers/GroupContent/types";
import { GroupDraftsView } from "scenes/Dashboard/containers/GroupDraftsView";
import { GroupEventsView } from "scenes/Dashboard/containers/GroupEventsView/index";
import { GroupFindingsView } from "scenes/Dashboard/containers/GroupFindingsView/index";
import { GroupForcesView } from "scenes/Dashboard/containers/GroupForcesView";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/GroupSettingsView/queries";
import type { IGroupData } from "scenes/Dashboard/containers/GroupSettingsView/Services/types";
import { GroupStakeholdersView } from "scenes/Dashboard/containers/GroupStakeholdersView/index";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/OrganizationContent/queries";
import { GET_ORG_LEVEL_PERMISSIONS } from "scenes/Dashboard/queries";
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
  const { groupName, organizationName } =
    useParams<{ groupName: string; organizationName: string }>();
  const { featurePreview } = useContext(featurePreviewContext);
  const [denyAccess, setDenyAccess] = useState(false);
  const [show, open, close] = useShow();
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canGetToeLines: boolean = permissions.can(
    "api_resolvers_group_toe_lines_resolve"
  );
  const canGetToeInputs: boolean = permissions.can(
    "api_resolvers_group_toe_inputs_resolve"
  );

  const continueAccess = useCallback((): void => {
    setDenyAccess(false);
  }, [setDenyAccess]);

  // GraphQL Operations
  const { data: orgData } = useQuery<IGetOrganizationId>(GET_ORGANIZATION_ID, {
    fetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred fetching organization ID", error);
      });
    },
    variables: {
      organizationName: organizationName.toLowerCase(),
    },
  });
  void useQuery<IGroupData>(GET_GROUP_DATA, {
    onCompleted: ({ group: { managed } }): void => {
      setDenyAccess(managed === "UNDER_REVIEW");
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorText"));
        Logger.warning("An error occurred getting group data", error);
      });
    },
    variables: { groupName },
  });
  const { data: orgPerms } = useQuery<IOrganizationPermission>(
    GET_ORG_LEVEL_PERMISSIONS,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((permissionsError: GraphQLError): void => {
          Logger.error(
            "Couldn't load group-level permissions",
            permissionsError
          );
        });
      },
      skip: orgData === undefined,
      variables: {
        identifier: orgData?.organizationId.id,
      },
    }
  );
  const { data } = useQuery<IGetEventStatus>(GET_GROUP_EVENT_STATUS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.warning("An error occurred loading event bar data", error);
        msgError(t("groupAlerts.errorTextsad"));
      });
    },
    variables: { groupName },
  });

  const events = useMemo(
    (): IGetEventStatus["group"]["events"] =>
      data === undefined ? [] : data.group.events,
    [data]
  );
  const hasOpenEvents = events.some(
    (event): boolean => event.eventStatus === "CREATED"
  );

  // Side effects
  useTabTracking("Group");

  if (_.isUndefined(orgData)) {
    return <div />;
  }
  const organizationId = orgData.organizationId.id;

  return (
    <StrictMode>
      {denyAccess ? (
        <div className={"flex justify-center mt5"}>
          <Card>
            <Text bright={0} mb={3} mt={3} tone={"red"}>
              <div className={"flex justify-center"}>
                <Lottie animationData={lotCircleXMark} size={100} />
              </div>
            </Text>
            <Text fw={7} mb={3} size={4} ta={"center"}>
              {t("group.accessDenied.title")}
            </Text>
            <Text mb={3} ta={"center"}>
              {t("group.accessDenied.text")}
              <Button onClick={open} size={"xs"}>
                <Text decor={["under"]}>{t("group.accessDenied.contact")}</Text>
              </Button>
              {t("group.accessDenied.moreInfo")}
            </Text>
            {orgPerms?.organization.userRole === "customer_manager" ? (
              <div className={"flex justify-center"}>
                <Button onClick={continueAccess} variant={"primary"}>
                  {t("group.accessDenied.btn")}
                </Button>
              </div>
            ) : undefined}
          </Card>
          <HelpModal onClose={close} open={show} />
        </div>
      ) : (
        <Fragment>
          <EventBar organizationName={organizationName} />
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
            <Tab
              id={"eventsTab"}
              link={`${url}/events`}
              tooltip={t("group.tabs.events.tooltip")}
            >
              {t("group.tabs.events.text")}
              {hasOpenEvents ? <Dot /> : undefined}
            </Tab>
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
            <groupContext.Provider value={{ organizationId, path, url }}>
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
        </Fragment>
      )}
    </StrictMode>
  );
};

export { GroupContent };
