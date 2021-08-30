import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import React from "react";
import { useParams } from "react-router-dom";

import { GitRoots } from "./GitRoots";
import { IPRoots } from "./IPRoots";
import { GET_ROOTS } from "./queries";
import type { Root } from "./types";
import { URLRoots } from "./URLRoots";
import { isGitRoot, isIPRoot, isURLRoot } from "./utils";

import { GroupSettingsView } from "../GroupSettingsView";
import { Have } from "utils/authz/Have";
import { Logger } from "utils/logger";

export const GroupScopeView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();

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
      <Have I={"has_service_white"}>
        <GitRoots
          groupName={groupName}
          onUpdate={refetch}
          roots={roots.filter(isGitRoot)}
        />
      </Have>
      <Have I={"has_service_black"}>
        <IPRoots
          groupName={groupName}
          onUpdate={refetch}
          roots={roots.filter(isIPRoot)}
        />
        <hr />
        <URLRoots
          groupName={groupName}
          onUpdate={refetch}
          roots={roots.filter(isURLRoot)}
        />
      </Have>
      <hr />
      <GroupSettingsView />
    </React.Fragment>
  );
};
