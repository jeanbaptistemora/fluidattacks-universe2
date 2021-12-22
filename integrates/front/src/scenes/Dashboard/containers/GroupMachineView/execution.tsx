import React from "react";

import type { IExecution } from "./types";

import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
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
    findingsExecuted,
    name,
    queue,
    rootId,
    rootNickname,
  } = props;

  const headersExecutionTable: IHeaderConfig[] = [
    {
      align: "center",
      dataField: "finding",
      header: translate.t("group.machine.finding.finding"),
    },
    {
      align: "center",
      dataField: "open",
      header: translate.t("group.machine.finding.open"),
    },
    {
      align: "center",
      dataField: "modified",
      header: translate.t("group.machine.finding.modified"),
      wrapped: true,
    },
  ];

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
        <Col33>
          <p>{name}</p>
        </Col33>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{translate.t("group.machine.job.queue")}</b>
          </p>
        </Col33>
        <Col33>
          <p>{queue}</p>
        </Col33>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{translate.t("group.machine.rootId")}</b>
          </p>
        </Col33>
        <Col60>
          <p>{rootId}</p>
        </Col60>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{translate.t("group.machine.root")}</b>
          </p>
        </Col33>
        <Col33>
          <p>{rootNickname}</p>
        </Col33>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{translate.t("group.machine.date.create")}</b>
          </p>
        </Col33>
        <Col33>
          <p>{formatDate(createdAt)}</p>
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
          <p>{formatDate(startedAt)}</p>
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
          <p>{formatDate(stoppedAt)}</p>
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
      <DataTableNext
        bordered={true}
        dataset={findingsExecuted}
        exportCsv={false}
        headers={headersExecutionTable}
        id={"tblMachineExecutions"}
        pageSize={100}
        search={false}
      />
      <br />
    </div>
  );
};

export { Execution };
