import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
import React from "react";
import { useTranslation } from "react-i18next";

import { GET_GIT_ROOT_DETAILS } from "../queries";
import type { IEnvironmentUrl } from "../types";
import { Col, Row } from "components/Layout";
import { formatIsoDate } from "utils/date";
import { Logger } from "utils/logger";

interface IDescriptionProps {
  cloningStatus: { message: string; status: string };
  environment: string;
  gitEnvironmentUrls: IEnvironmentUrl[];
  gitignore: string[];
  id: string;
  nickname: string;
}

const Description = ({
  cloningStatus,
  environment,
  gitEnvironmentUrls,
  gitignore,
  groupName,
  id,
  nickname,
}: IDescriptionProps & { groupName: string }): JSX.Element => {
  const { t } = useTranslation();

  // GraphQL operations
  const { data } = useQuery<{
    root: {
      lastCloningStatusUpdate: string;
      lastStateStatusUpdate: string;
    };
  }>(GET_GIT_ROOT_DETAILS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load root details", error);
      });
    },
    variables: { groupName, rootId: id },
  });
  const rootDetails =
    data === undefined
      ? {
          lastCloningStatusUpdate: "",
          lastStateStatusUpdate: "",
        }
      : data.root;
  const { lastCloningStatusUpdate, lastStateStatusUpdate } = rootDetails;

  return (
    <div>
      <h3>{t("group.findings.description.title")}</h3>
      <Row>
        <Col>
          {t("group.scope.git.repo.nickname")}
          {":"}&nbsp;{nickname}
        </Col>
        <Col>
          {t("group.scope.git.repo.environment")}
          {":"}&nbsp;{environment}
        </Col>
      </Row>
      <hr />
      <Row>
        <Col>
          {t("group.scope.git.envUrls")}
          {":"}
          <ul>
            {gitEnvironmentUrls.map(
              (envUrl): JSX.Element => (
                <li key={envUrl.id}>
                  <a href={envUrl.url} rel={"noreferrer"} target={"_blank"}>
                    {envUrl.url}
                  </a>
                </li>
              )
            )}
          </ul>
        </Col>
        <Col>
          {t("group.scope.git.filter.exclude")}
          {":"}
          <ul>
            {gitignore.map(
              (pattern): JSX.Element => (
                <li key={pattern}>{pattern}</li>
              )
            )}
          </ul>
        </Col>
      </Row>
      <hr />
      <Row>
        <Col>
          {t("group.scope.common.lastStateStatusUpdate")}
          {":"}&nbsp;{formatIsoDate(lastStateStatusUpdate)}
        </Col>
        <Col>
          {t("group.scope.common.lastCloningStatusUpdate")}
          {":"}&nbsp;{formatIsoDate(lastCloningStatusUpdate)}
        </Col>
      </Row>
      <hr />
      <Row>
        <Col>
          {t("group.scope.git.repo.cloning.message")}
          {":"}&nbsp;{cloningStatus.message}
        </Col>
      </Row>
    </div>
  );
};

export const renderDescriptionComponent = (
  props: IDescriptionProps,
  groupName: string
): JSX.Element => (
  <Description
    cloningStatus={props.cloningStatus}
    environment={props.environment}
    gitEnvironmentUrls={props.gitEnvironmentUrls}
    gitignore={props.gitignore}
    groupName={groupName}
    id={props.id}
    nickname={props.nickname}
  />
);
