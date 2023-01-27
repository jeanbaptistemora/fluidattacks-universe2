import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import {
  faBriefcase,
  faChartSimple,
  faFileLines,
  faFolder,
  faIdCard,
  faMoneyBill,
  faShield,
  faUsers,
} from "@fortawesome/free-solid-svg-icons";
import type { GraphQLError } from "graphql";
import React, { Fragment } from "react";
import type { FC } from "react";
import { useTranslation } from "react-i18next";
import { Route, useParams } from "react-router-dom";

import { GroupTabs } from "./GroupTabs";
import { GET_ORG_GROUPS } from "./queries";
import type { IGetOrganizationGroups, IGroupData } from "./types";

import { SideBarSubTabs, SideBarTab } from "components/SideBar";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const OrganizationTabs: FC = (): JSX.Element => {
  const { org } = useParams<{ org: string }>();
  const { t } = useTranslation();

  const { data: DataOrgs } = useQuery<IGetOrganizationGroups>(GET_ORG_GROUPS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading organization groups", error);
      });
    },
    variables: { org },
  });

  const dataGroups: IGroupData[] = DataOrgs
    ? DataOrgs.organizationId.groups
    : [];

  const groupTip = `${t("organization.tabs.groups.text")} (${
    dataGroups.length
  })`;

  return (
    <Fragment>
      <SideBarSubTabs>
        <SideBarTab icon={faFolder} tip={groupTip} to={`/orgs/${org}/groups`} />
        <Route path={"/orgs/:org/groups/:group/"}>
          <GroupTabs />
        </Route>
      </SideBarSubTabs>
      <SideBarTab
        icon={faChartSimple}
        tip={t("organization.tabs.analytics.text")}
        to={`/orgs/${org}/analytics`}
      />
      <SideBarTab
        icon={faShield}
        tip={t("organization.tabs.policies.text")}
        to={`/orgs/${org}/policies`}
      />
      <SideBarTab
        icon={faUsers}
        tip={t("organization.tabs.users.text")}
        to={`/orgs/${org}/stakeholders`}
      />
      <SideBarTab
        icon={faBriefcase}
        tip={t("organization.tabs.portfolios.text")}
        to={`/orgs/${org}/portfolios`}
      />
      <SideBarTab
        icon={faIdCard}
        tip={t("organization.tabs.credentials.text")}
        to={`/orgs/${org}/credentials`}
      />
      <SideBarTab
        icon={faFileLines}
        tip={t("organization.tabs.compliance.text")}
        to={`/orgs/${org}/compliance`}
      />
      <Can do={"api_resolvers_organization_billing_resolve"}>
        <SideBarTab
          icon={faMoneyBill}
          tip={t("organization.tabs.billing.text")}
          to={`/orgs/${org}/billing`}
        />
      </Can>
    </Fragment>
  );
};

export { OrganizationTabs };
