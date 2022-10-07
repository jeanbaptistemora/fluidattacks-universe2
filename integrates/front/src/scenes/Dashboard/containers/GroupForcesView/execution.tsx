/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import type { ColumnDef } from "@tanstack/react-table";
import _ from "lodash";
import React from "react";
import ReactAnsi from "react-ansi";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route, Switch } from "react-router-dom";

import { Table } from "components/TableNew";
import { Tab, Tabs } from "components/Tabs";
import styles from "scenes/Dashboard/containers/GroupForcesView/index.css";
import { GET_FORCES_EXECUTION } from "scenes/Dashboard/containers/GroupForcesView/queries";
import type {
  IExecution,
  IExploitResult,
  IFoundVulnerabilities,
  IGetForcesExecution,
} from "scenes/Dashboard/containers/GroupForcesView/types";
import { Col33, Row, TabContent } from "styles/styledComponents";

const Execution: React.FC<IExecution> = (
  props: Readonly<IExecution>
): JSX.Element => {
  const { t } = useTranslation();
  const { log, executionId, groupName } = props;
  const isOld: boolean = log !== undefined;

  const { loading, data } = useQuery<IGetForcesExecution>(
    GET_FORCES_EXECUTION,
    {
      skip: isOld,
      variables: {
        executionId,
        groupName,
      },
    }
  );

  if (loading && !isOld) {
    return <p>{"Loading ..."}</p>;
  }

  const execution: IExecution = isOld
    ? props
    : { ...props, ...data?.forcesExecution };

  const stateResolve: (status: string) => string = (status: string): string => {
    switch (status) {
      case "OPEN":
        return t("group.forces.status.vulnerable");
      case "CLOSED":
        return t("group.forces.status.secure");
      case "ACCEPTED":
        return t("group.forces.status.accepted");
      default:
        return "";
    }
  };

  const getVulnerabilitySummaries: (
    foundVulnerabilities: IFoundVulnerabilities
  ) => string = (foundVulnerabilities: IFoundVulnerabilities): string => {
    const openTrans: string = t("group.forces.foundVulnerabilitiesNew.open");
    const acceptedTrans: string = t(
      "group.forces.foundVulnerabilitiesNew.accepted"
    );
    const closedTrans: string = t(
      "group.forces.foundVulnerabilitiesNew.closed"
    );
    const totalTrans: string = t("group.forces.foundVulnerabilitiesNew.total");

    const openStr: string = `${foundVulnerabilities.open} ${openTrans}`;
    const acceptedStr: string = `${foundVulnerabilities.accepted} ${acceptedTrans}`;
    const closedStr: string = `${foundVulnerabilities.closed} ${closedTrans}`;
    const totalStr: string = `${foundVulnerabilities.total} ${totalTrans}`;

    return `${openStr}, ${acceptedStr}, ${closedStr}, ${totalStr}`;
  };

  const vulns: IExploitResult[] = _.isNull(execution.vulnerabilities)
    ? []
    : execution.vulnerabilities.open.concat(
        execution.vulnerabilities.closed.concat(
          execution.vulnerabilities.accepted
        )
      );

  const datset = vulns.map(
    (elem: IExploitResult): IExploitResult => ({
      ...elem,
      state: stateResolve(elem.state),
    })
  );

  const columns: ColumnDef<IExploitResult>[] = [
    {
      accessorFn: (row): number => row.exploitability,
      header: t("group.forces.compromisedToe.exploitability"),
      id: "explotability",
      meta: { filterType: "select" },
    },
    {
      accessorFn: (row): string => row.state,
      header: t("group.forces.compromisedToe.status"),
      id: "state",
      meta: { filterType: "select" },
    },
    {
      accessorFn: (row): string => row.kind,

      header: t("group.forces.compromisedToe.type"),
      id: "kind",
      meta: { filterType: "select" },
    },
    {
      accessorFn: (row): string => row.who,
      header: t("group.forces.compromisedToe.what"),
      id: "who",
      meta: { filterType: "select" },
    },
    {
      accessorFn: (row): string => row.where,
      header: t("group.forces.compromisedToe.where"),
      id: "where",
      meta: { filterType: "select" },
    },
  ];

  return (
    <div>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{t("group.forces.date")}</b>
          </p>
        </Col33>
        <Col33>
          <p>{execution.date}</p>
        </Col33>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{t("group.forces.status.title")}</b>
          </p>
        </Col33>
        <Col33>
          <p>{execution.status}</p>
        </Col33>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{t("group.forces.strictness.title")}</b>
          </p>
        </Col33>
        <Col33>
          <p>{execution.strictness}</p>
        </Col33>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{t("group.forces.severityThreshold.title")}</b>
          </p>
        </Col33>
        <Col33>
          <p>{execution.severityThreshold}</p>
        </Col33>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{t("group.forces.gracePeriod.title")}</b>
          </p>
        </Col33>
        <Col33>
          <p>{execution.gracePeriod}</p>
        </Col33>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{t("group.forces.kind.title")}</b>
          </p>
        </Col33>
        <Col33>
          <p>{execution.kind}</p>
        </Col33>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{t("group.forces.gitRepo")}</b>
          </p>
        </Col33>
        <Col33>
          <p>{execution.gitRepo}</p>
        </Col33>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{t("group.forces.identifier")}</b>
          </p>
        </Col33>
        <Col33>
          <p>{execution.executionId}</p>
        </Col33>
      </Row>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <Row className={"nb3"}>
        <Col33>
          <p>
            <b>{t("group.forces.foundVulnerabilities.title")}</b>
          </p>
        </Col33>
        <Col33>
          <p className={styles.wrapped}>
            {getVulnerabilitySummaries(execution.foundVulnerabilities)}
          </p>
        </Col33>
      </Row>
      <br />
      <MemoryRouter initialEntries={["/summary"]} initialIndex={0}>
        <Tabs>
          <Tab
            id={"forcesExecutionSummaryTab"}
            link={"/summary"}
            tooltip={t("group.forces.tabs.summary.tooltip")}
          >
            {t("group.forces.tabs.summary.text")}
          </Tab>
          <Tab
            id={"forcesExecutionLogTab"}
            link={"/log"}
            tooltip={t("group.forces.tabs.log.tooltip")}
          >
            {t("group.forces.tabs.log.text")}
          </Tab>
        </Tabs>
        <TabContent>
          <Switch>
            <Route path={"/summary"}>
              <Table
                columnToggle={true}
                columns={columns}
                data={datset}
                enableColumnFilters={true}
                enableSearchBar={true}
                exportCsv={false}
                id={"tblCompromisedToe"}
              />
            </Route>
            <Route path={"/log"}>
              <ReactAnsi autoScroll={true} log={execution.log as string} />
            </Route>
          </Switch>
        </TabContent>
      </MemoryRouter>
    </div>
  );
};

export { Execution };
