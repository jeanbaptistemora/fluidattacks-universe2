import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import React, { Fragment } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { GitRoots } from "./GitRoots";
import { GroupSettingsView } from "./GroupSettingsView";
import { IPRoots } from "./IPRoots";
import { GET_ROOTS } from "./queries";
import type { Root } from "./types";
import { URLRoots } from "./URLRoots";
import { isGitRoot, isIPRoot, isURLRoot, mapInactiveStatus } from "./utils";

import { Card } from "components/Card";
import { Text } from "components/Text";
import { Have } from "utils/authz/Have";
import { Logger } from "utils/logger";

export const GroupScopeView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();

  // GraphQL operations
  const { data, refetch } = useQuery<{
    group: { roots: Root[] };
  }>(GET_ROOTS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load roots", error);
      });
    },
    variables: { groupName },
  });
  const roots: Root[] = data === undefined ? [] : data.group.roots;

  return (
    <Fragment>
      <Have I={"has_service_white"}>
        <GitRoots
          groupName={groupName}
          onUpdate={refetch}
          roots={mapInactiveStatus(roots.filter(isGitRoot))}
        />
      </Have>
      <Have I={"has_service_black"}>
        <Text fw={7} mb={3} mt={4} size={"big"}>
          {t("group.scope.ip.title")}
        </Text>
        <Card>
          <IPRoots
            groupName={groupName}
            onUpdate={refetch}
            roots={roots.filter(isIPRoot)}
          />
        </Card>
        <Text fw={7} mb={3} mt={4} size={"big"}>
          {t("group.scope.url.title")}
        </Text>
        <Card>
          <URLRoots
            groupName={groupName}
            onUpdate={refetch}
            roots={roots.filter(isURLRoot)}
          />
        </Card>
      </Have>
      <GroupSettingsView />
    </Fragment>
  );
};
