import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
import React from "react";
import { useTranslation } from "react-i18next";

import { GET_GIT_ROOT_DETAILS } from "../queries";
import { Col50, Row } from "styles/styledComponents";
import { formatIsoDate } from "utils/date";
import { Logger } from "utils/logger";

interface ILastMachineExecutions {
  complete: {
    stoppedAt: string | null;
  } | null;
  specific: {
    findingsExecuted: {
      finding: string;
    }[];
    stoppedAt: string | null;
  } | null;
}

interface IDescriptionProps {
  cloningStatus: { message: string };
  environment: string;
  environmentUrls: string[];
  gitignore: string[];
  id: string;
  nickname: string;
}

const Description = ({
  cloningStatus,
  environment,
  environmentUrls,
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
      lastMachineExecutions: ILastMachineExecutions;
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
          lastMachineExecutions: {
            complete: null,
            specific: null,
          },
          lastStateStatusUpdate: "",
        }
      : data.root;
  const {
    lastCloningStatusUpdate,
    lastMachineExecutions,
    lastStateStatusUpdate,
  } = rootDetails;

  return (
    <div>
      <h3>{t("group.findings.description.title")}</h3>
      <Row>
        <Col50>
          {t("group.scope.git.repo.nickname")}
          {":"}&nbsp;{nickname}
        </Col50>
        <Col50>
          {t("group.scope.git.repo.environment")}
          {":"}&nbsp;{environment}
        </Col50>
      </Row>
      <hr />
      <Row>
        <Col50>
          {t("group.scope.git.envUrls")}
          {":"}
          <ul>
            {environmentUrls.map(
              (url): JSX.Element => (
                <li key={url}>{url}</li>
              )
            )}
          </ul>
        </Col50>
        <Col50>
          {t("group.scope.git.filter.exclude")}
          {":"}
          <ul>
            {gitignore.map(
              (pattern): JSX.Element => (
                <li key={pattern}>{pattern}</li>
              )
            )}
          </ul>
        </Col50>
      </Row>
      <hr />
      <Row>
        <Col50>
          {t("group.scope.common.lastStateStatusUpdate")}
          {":"}&nbsp;{formatIsoDate(lastStateStatusUpdate)}
        </Col50>
        <Col50>
          {t("group.scope.common.lastCloningStatusUpdate")}
          {":"}&nbsp;{formatIsoDate(lastCloningStatusUpdate)}
        </Col50>
      </Row>
      <hr />
      <Row>
        <Col50>
          {t("group.scope.git.repo.cloning.message")}
          {":"}&nbsp;{cloningStatus.message}
        </Col50>
      </Row>
      <hr />
      <Row>
        <Col50>
          {t("group.scope.git.repo.machineExecutions.messageComplete")}
          {":"}&nbsp;
          {lastMachineExecutions.complete === null
            ? t("group.scope.git.repo.machineExecutions.noExecutions")
            : lastMachineExecutions.complete.stoppedAt === null
            ? t("group.scope.git.repo.machineExecutions.active")
            : lastMachineExecutions.complete.stoppedAt}
        </Col50>
        <Col50>
          {t("group.scope.git.repo.machineExecutions.messageSpecific")}
          {":"}&nbsp;
          {lastMachineExecutions.specific === null
            ? t("group.scope.git.repo.machineExecutions.noExecutions")
            : lastMachineExecutions.specific.stoppedAt === null
            ? `${t("group.scope.git.repo.machineExecutions.active")} for ${
                lastMachineExecutions.specific.findingsExecuted[0].finding
              }`
            : `${lastMachineExecutions.specific.findingsExecuted[0].finding} on ${lastMachineExecutions.specific.stoppedAt}`}
        </Col50>
      </Row>
    </div>
  );
};

const renderDescriptionComponent = (
  props: IDescriptionProps,
  groupName: string
): JSX.Element => (
  <Description
    cloningStatus={props.cloningStatus}
    environment={props.environment}
    environmentUrls={props.environmentUrls}
    gitignore={props.gitignore}
    groupName={groupName}
    id={props.id}
    nickname={props.nickname}
  />
);

export const renderRepoDescription =
  (groupName: string): ((props: IDescriptionProps) => JSX.Element) =>
  (props: IDescriptionProps): JSX.Element =>
    renderDescriptionComponent(props, groupName);
