import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import React from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { GitRoots } from "./GitRoots";
import { IPRoots } from "./IPRoots";
import { GET_ROOTS } from "./queries";
import type { Root } from "./types";
import { URLRoots } from "./URLRoots";
import { isGitRoot, isIPRoot, isURLRoot, mapInactiveStatus } from "./utils";

import { GroupSettingsView } from "../GroupSettingsView";
import { Card } from "components/Card";
import { Col, Row } from "components/Layout";
import { Have } from "utils/authz/Have";
import { Logger } from "utils/logger";

export const GroupScopeView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();

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
    <Row>
      <Have I={"has_service_white"}>
        <Col>
          <Card title={t("group.scope.git.title")}>
            <GitRoots
              groupName={groupName}
              onUpdate={refetch}
              roots={mapInactiveStatus(roots.filter(isGitRoot))}
            />
          </Card>
        </Col>
      </Have>
      <Have I={"has_service_black"}>
        <Col>
          <Card title={t("group.scope.ip.title")}>
            <IPRoots
              groupName={groupName}
              onUpdate={refetch}
              roots={roots.filter(isIPRoot)}
            />
          </Card>
        </Col>
        <Col>
          <Card title={t("group.scope.url.title")}>
            <URLRoots
              groupName={groupName}
              onUpdate={refetch}
              roots={roots.filter(isURLRoot)}
            />
          </Card>
        </Col>
      </Have>
      <Col>
        <GroupSettingsView />
      </Col>
    </Row>
  );
};
