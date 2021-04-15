import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import React from "react";
import { useParams } from "react-router";

import { GitRoots } from "./GitRoots";
import { GET_ROOTS } from "./queries";
import type { IGitRootAttr, Root } from "./types";

import { ProjectSettingsView } from "../ProjectSettingsView";
import { Have } from "utils/authz/Have";
import { Logger } from "utils/logger";

const isGitRoot = (root: Root): root is IGitRootAttr =>
  root.__typename === "GitRoot";

export const GroupScopeView: React.FC = (): JSX.Element => {
  const { projectName: groupName } = useParams<{ projectName: string }>();

  // GraphQL operations
  const { data, refetch } = useQuery<{ group: { roots: Root[] } }>(GET_ROOTS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load roots", error);
      });
    },
    variables: { groupName },
  });
  const roots: Root[] = data === undefined ? [] : data.group.roots;

  return (
    <React.Fragment>
      <Have I={"has_drills_white"}>
        <GitRoots
          groupName={groupName}
          onUpdate={refetch}
          roots={roots.filter(isGitRoot)}
        />
      </Have>
      <hr />
      <ProjectSettingsView />
    </React.Fragment>
  );
};
