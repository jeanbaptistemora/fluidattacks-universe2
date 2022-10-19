/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */
import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import {
  faChartSimple,
  faFileLines,
  faFolder,
  faShield,
} from "@fortawesome/free-solid-svg-icons";
import type { GraphQLError } from "graphql";
import React, { Fragment } from "react";
import type { FC } from "react";
import { useTranslation } from "react-i18next";
import { Route, useParams } from "react-router-dom";

import { GroupTabs } from "./GroupTabs";
import { GET_GROUP_VULNS } from "./queries";
import type { IGetOrganizationGroups, IGroupData } from "./types";

import { SideBarSubTabs, SideBarTab } from "components/SideBar";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const OrganizationTabs: FC = (): JSX.Element => {
  const { org } = useParams<{ org: string }>();
  const { t } = useTranslation();

  const { data } = useQuery<IGetOrganizationGroups>(GET_GROUP_VULNS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading organization groups", error);
      });
    },
    variables: { org },
  });
  const dataset: IGroupData[] = data ? data.organizationId.groups : [];

  return (
    <Fragment>
      <SideBarSubTabs>
        <SideBarTab icon={faFolder} to={`/orgs/${org}/groups`}>
          {`Groups (${dataset.length})`}
        </SideBarTab>
        <Route path={"/orgs/:org/groups/:group/"}>
          <GroupTabs />
        </Route>
      </SideBarSubTabs>
      <SideBarTab icon={faChartSimple} to={`/orgs/${org}/analytics`}>
        {"Analytics"}
      </SideBarTab>
      <SideBarTab icon={faShield} to={`/orgs/${org}/policies`}>
        {"Policies"}
      </SideBarTab>
      <SideBarTab icon={faFileLines} to={`/orgs/${org}/compliance`}>
        {"Compliance"}
      </SideBarTab>
    </Fragment>
  );
};

export { OrganizationTabs };
