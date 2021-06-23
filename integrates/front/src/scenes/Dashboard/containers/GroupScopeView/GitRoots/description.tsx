import React from "react";
import { useTranslation } from "react-i18next";

import { Col50, Row } from "styles/styledComponents";

interface IDescriptionProps {
  cloningStatus: { message: string };
  environment: string;
  environmentUrls: string[];
  gitignore: string[];
  lastCloningStatusUpdate: string;
  lastStateStatusUpdate: string;
  nickname: string;
}

const Description = ({
  cloningStatus,
  environment,
  environmentUrls,
  gitignore,
  lastCloningStatusUpdate,
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
          {":"}&nbsp;{lastStateStatusUpdate}
        </Col50>
        <Col50>
          {t("group.scope.common.lastCloningStatusUpdate")}
          {":"}&nbsp;{lastCloningStatusUpdate}
        </Col50>
      </Row>
      <hr />
      <Row>
        <Col50>
          {t("group.scope.git.repo.cloning.message")}
          {":"}&nbsp;{cloningStatus.message}
        </Col50>
      </Row>
    </div>
  );
};

export const renderDescription = (props: IDescriptionProps): JSX.Element => (
  <Description
    cloningStatus={props.cloningStatus}
    environment={props.environment}
    environmentUrls={props.environmentUrls}
    gitignore={props.gitignore}
    lastCloningStatusUpdate={props.lastCloningStatusUpdate}
    lastStateStatusUpdate={props.lastStateStatusUpdate}
    nickname={props.nickname}
  />
);
