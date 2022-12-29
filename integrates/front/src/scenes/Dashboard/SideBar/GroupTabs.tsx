import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import type { FC } from "react";
import React, { useEffect, useMemo } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { SideBarTab } from "components/SideBar";
import { GET_VULNERABLE_GROUP_VULNS } from "scenes/Dashboard/SideBar/queries";
import type { IGroupTabVulns, INodeData } from "scenes/Dashboard/SideBar/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const GroupTabs: FC = (): JSX.Element => {
  const { group, org } = useParams<{ group: string; org: string }>();
  const { t } = useTranslation();

  const { data, fetchMore } = useQuery<IGroupTabVulns>(
    GET_VULNERABLE_GROUP_VULNS,
    {
      fetchPolicy: "no-cache",
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred loading organization groups",
            error
          );
        });
      },
      variables: { first: 150, group },
    }
  );

  const filteredData: INodeData[] = useMemo(
    (): INodeData[] =>
      (data ? data.group.vulnerabilities.edges : []).filter(
        (node: INodeData): boolean =>
          (node.node.zeroRisk === "Rejected" ||
            _.isEmpty(node.node.zeroRisk)) &&
          node.node.state === "VULNERABLE"
      ),
    [data]
  );
  const hasNextPage = useMemo(
    (): boolean =>
      data === undefined
        ? true
        : data.group.vulnerabilities.pageInfo.hasNextPage,
    [data]
  );
  const length = useMemo(
    (): number =>
      hasNextPage
        ? data?.group.vulnerabilities.total ?? 0
        : filteredData.length,
    [filteredData, data, hasNextPage]
  );
  const tip = useMemo(
    (): string =>
      `${t("organization.tabs.groups.vulnerabilities.header")} (${length})`,
    [length, t]
  );
  useEffect((): void => {
    if (!_.isUndefined(data)) {
      if (data.group.vulnerabilities.pageInfo.hasNextPage) {
        void fetchMore({
          variables: {
            after: data.group.vulnerabilities.pageInfo.endCursor,
          },
        });
      }
    }
  }, [data, fetchMore]);

  return (
    <SideBarTab
      icon={faMagnifyingGlass}
      tip={tip}
      to={`/orgs/${org}/groups/${group}/vulns`}
    />
  );
};

export { GroupTabs };
