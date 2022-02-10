import React from "react";
import { useTranslation } from "react-i18next";

import { Col50, Row } from "styles/styledComponents";
import { formatIsoDate } from "utils/date";

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
  lastCloningStatusUpdate: string;
  lastMachineExecutions: ILastMachineExecutions;
  lastStateStatusUpdate: string;
  nickname: string;
}

const Description = ({
  cloningStatus,
  environment,
  environmentUrls,
  gitignore,
  lastCloningStatusUpdate,
  lastMachineExecutions,
  lastStateStatusUpdate,
  nickname,
}: IDescriptionProps): JSX.Element => {
  const { t } = useTranslation();

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

export const renderRepoDescription = (
  props: IDescriptionProps
): JSX.Element => (
  <Description
    cloningStatus={props.cloningStatus}
    environment={props.environment}
    environmentUrls={props.environmentUrls}
    gitignore={props.gitignore}
    lastCloningStatusUpdate={props.lastCloningStatusUpdate}
    lastMachineExecutions={props.lastMachineExecutions}
    lastStateStatusUpdate={props.lastStateStatusUpdate}
    nickname={props.nickname}
  />
);
