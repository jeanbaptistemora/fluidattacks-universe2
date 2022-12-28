import _ from "lodash";
import React from "react";

import type { IExecution } from "./types";

import { Col33, Col60, Row } from "styles/styledComponents";
import { formatDate, formatDuration } from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

const Execution: React.FC<IExecution> = (
  props: Readonly<IExecution>
): JSX.Element => {
  const {
    jobId,
    createdAt,
    startedAt,
    stoppedAt,
    duration,
    name,
    rootNickname,
    vulnerabilities,
  } = props;

  return (
    <div>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{translate.t("group.machine.job.id")}</b>
          </p>
        </Col33>
        <Col60>
          <p>{jobId}</p>
        </Col60>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{translate.t("group.machine.job.name")}</b>
          </p>
        </Col33>
        <Col60>
          <p>{name}</p>
        </Col60>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{translate.t("group.machine.root")}</b>
          </p>
        </Col33>
        <Col60>
          <p>{rootNickname}</p>
        </Col60>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{translate.t("group.machine.date.create")}</b>
          </p>
        </Col33>
        <Col33>
          <p>{createdAt === null ? "" : formatDate(parseFloat(createdAt))}</p>
        </Col33>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{translate.t("group.machine.date.start")}</b>
          </p>
        </Col33>
        <Col33>
          <p>{startedAt === null ? "" : formatDate(parseFloat(startedAt))}</p>
        </Col33>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{translate.t("group.machine.date.stop")}</b>
          </p>
        </Col33>
        <Col33>
          <p>{stoppedAt === null ? "" : formatDate(parseFloat(stoppedAt))}</p>
        </Col33>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{translate.t("group.machine.date.duration")}</b>
          </p>
        </Col33>
        <Col33>
          <p>{formatDuration(duration)}</p>
        </Col33>
      </Row>
      {!_.isUndefined(vulnerabilities) && (
        <React.Fragment>
          {/* eslint-disable-next-line react/forbid-component-props */}
          <Row className={"nb3"}>
            <Col33>
              <p>
                <b>{"Open vulnerabilities"}</b>
              </p>
            </Col33>
            <Col33>
              <p>{vulnerabilities?.open}</p>
            </Col33>
          </Row>
          {/* eslint-disable-next-line react/forbid-component-props */}
          <Row className={"nb3"}>
            <Col33>
              <p>
                <b>{"Modified vulnerabilities"}</b>
              </p>
            </Col33>
            <Col33>
              <p>{vulnerabilities?.modified}</p>
            </Col33>
          </Row>
        </React.Fragment>
      )}
      <br />
    </div>
  );
};

export { Execution };
