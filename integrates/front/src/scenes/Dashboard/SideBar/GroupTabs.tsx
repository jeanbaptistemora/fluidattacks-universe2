import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import type { FC } from "react";
import React from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { GET_GROUP_VULNS } from "./queries";
import type { IGroupTabVulns, INodeData } from "./types";

import { SideBarTab } from "components/SideBar";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const GroupTabs: FC = (): JSX.Element => {
  const { group, org } = useParams<{ group: string; org: string }>();
  const { t } = useTranslation();

  const { data } = useQuery<IGroupTabVulns>(GET_GROUP_VULNS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading organization groups", error);
      });
    },
    variables: { group },
  });
  const dataset: INodeData[] = data ? data.group.vulnerabilities.edges : [];
  const filteredData = dataset.filter(
    (node: INodeData): boolean =>
      (node.node.zeroRisk === "Rejected" || _.isEmpty(node.node.zeroRisk)) &&
      node.node.currentState === "open"
  );

  return (
    <SideBarTab to={`/orgs/${org}/groups/${group}/vulns`}>
      {`Vulnerabilities (${filteredData.length})`}
    </SideBarTab>
  );
};

export { GroupTabs };
