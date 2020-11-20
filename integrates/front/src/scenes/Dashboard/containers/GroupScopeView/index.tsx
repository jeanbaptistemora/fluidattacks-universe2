import type { ApolloError } from "apollo-client";
import { DataTableNext } from "components/DataTableNext";
import { GET_ROOTS } from "./query";
import type { GraphQLError } from "graphql";
import { Logger } from "utils/logger";
import React from "react";
import { useParams } from "react-router";
import { useQuery } from "@apollo/react-hooks";
import { useTranslation } from "react-i18next";
import type { IGitRootAttr, Root } from "./types";

export const GroupScopeView: React.FC = (): JSX.Element => {
  const { projectName: groupName } = useParams<{ projectName: string }>();
  const { t } = useTranslation();

  // GraphQL operations
  const { data } = useQuery<{ group: { roots: Root[] } }>(GET_ROOTS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load roots", error);
      });
    },
    variables: { groupName },
  });
  const roots: Root[] = data === undefined ? [] : data.group.roots;

  const gitRoots: IGitRootAttr[] = roots.filter(
    (root: Root): boolean => root.__typename === "GitRoot"
  ) as IGitRootAttr[];

  return (
    <DataTableNext
      bordered={false}
      dataset={gitRoots}
      exportCsv={false}
      headers={[
        { dataField: "url", header: t("group.scope.table.url") },
        { dataField: "branch", header: t("group.scope.table.branch") },
      ]}
      id={"tblGitRoots"}
      pageSize={15}
      search={true}
      striped={true}
    />
  );
};
