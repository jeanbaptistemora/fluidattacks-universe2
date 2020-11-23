import type { ApolloError } from "apollo-client";
import { GET_ROOTS } from "./query";
import { GitRoots } from "./GitRoots";
import type { GraphQLError } from "graphql";
import { Have } from "utils/authz/Have";
import { Logger } from "utils/logger";
import React from "react";
import { useParams } from "react-router";
import { useQuery } from "@apollo/react-hooks";
import type { IGitRootAttr, Root } from "./types";

const isGitRoot: (root: Root) => root is IGitRootAttr = (
  root: Root
): root is IGitRootAttr => root.__typename === "GitRoot";

export const GroupScopeView: React.FC = (): JSX.Element => {
  const { projectName: groupName } = useParams<{ projectName: string }>();

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

  return (
    <Have I={"has_drills_white"}>
      <GitRoots roots={roots.filter(isGitRoot)} />
    </Have>
  );
};
