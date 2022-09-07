/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import _ from "lodash";
import type { ReactElement } from "react";
import React, { useCallback, useState } from "react";
import { selectFilter } from "react-bootstrap-table2-filter";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route, Switch } from "react-router-dom";
import SyntaxHighlighter from "react-syntax-highlighter/dist/esm/light";
import monokaiSublime from "react-syntax-highlighter/dist/esm/styles/hljs/monokai-sublime";

import { Table } from "components/Table";
import type { IHeaderConfig } from "components/Table/types";
import { filterSearchText } from "components/Table/utils";
import { Tab, Tabs } from "components/Tabs";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import styles from "scenes/Dashboard/containers/GroupForcesView/index.css";
import { GET_FORCES_EXECUTION } from "scenes/Dashboard/containers/GroupForcesView/queries";
import type {
  IExecution,
  IExploitResult,
  IFoundVulnerabilities,
  IGetForcesExecution,
  IVulnerabilities,
} from "scenes/Dashboard/containers/GroupForcesView/types";
import { Col33, Row, TabContent } from "styles/styledComponents";
import { useStoredState } from "utils/hooks";

const Execution: React.FC<IExecution> = (
  props: Readonly<IExecution>
): JSX.Element => {
  const { t } = useTranslation();
  const { log, executionId, groupName } = props;
  const isOld: boolean = log !== undefined;

  const [isFilterEnabled, setFilterEnabled] = useStoredState<boolean>(
    "forcesExecutionFilters",
    false
  );
  const [searchTextFilter, setSearchTextFilter] = useState("");

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

  const handleUpdateFilter: () => void = useCallback((): void => {
    setFilterEnabled(!isFilterEnabled);
  }, [isFilterEnabled, setFilterEnabled]);

  if (loading && !isOld) {
    return <p>{"Loading ..."}</p>;
  }

  const selectOptionsStatus = { Secure: "Secure", Vulnerable: "Vulnerable" };
  const selectOptionsKind = { DAST: "DAST", SAST: "SAST" };
  const selectOptionsExploitability = {
    Functional: "Functional",
    High: "High",
    "Proof of concept": "Proof of concept",
    Unproven: "Unproven",
  };

  const execution: IExecution = isOld
    ? props
    : { ...props, ...data?.forcesExecution };

  const onFilterStatus: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("statusExecutionFilter", filterVal);
  };
  const onFilterKind: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("kindExecutionFilter", filterVal);
  };
  const onFilterExploitability: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("exploitabilityForcesFilter", filterVal);
  };
  const formatText: (text: string) => ReactElement<Text> = (
    text: string
  ): ReactElement<Text> => <p className={styles.wrapped}>{text}</p>;

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

  const getDatasetFromVulnerabilities: (
    vulnerabilities: IVulnerabilities | null
  ) => Record<string, unknown>[] = (
    vulnerabilities: IVulnerabilities | null
  ): Record<string, unknown>[] => {
    const vulns: IExploitResult[] = _.isNull(vulnerabilities)
      ? []
      : vulnerabilities.open.concat(
          vulnerabilities.closed.concat(vulnerabilities.accepted)
        );

    return vulns.map(
      (elem: IExploitResult): Record<string, unknown> => ({
        ...elem,
        state: stateResolve(elem.state),
      })
    );
  };

  const headersCompromisedToeTable: IHeaderConfig[] = [
    {
      dataField: "exploitability",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "exploitabilityForcesFilter"),
        onFilter: onFilterExploitability,
        options: selectOptionsExploitability,
      }),
      formatter: formatText,
      header: t("group.forces.compromisedToe.exploitability"),
      width: "15%",
      wrapped: true,
    },
    {
      dataField: "state",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "statusExecutionFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: statusFormatter,
      header: t("group.forces.compromisedToe.status"),
      width: "105px",
      wrapped: true,
    },
    {
      dataField: "kind",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "kindExecutionFilter"),
        onFilter: onFilterKind,
        options: selectOptionsKind,
      }),
      formatter: formatText,
      header: t("group.forces.compromisedToe.type"),
      width: "10%",
      wrapped: true,
    },
    {
      dataField: "who",
      formatter: formatText,
      header: t("group.forces.compromisedToe.what"),
      wrapped: true,
    },
    {
      dataField: "where",
      formatter: formatText,
      header: t("group.forces.compromisedToe.where"),
      wrapped: true,
    },
  ];

  const filterSearchtextResult: Record<string, unknown>[] = filterSearchText(
    getDatasetFromVulnerabilities(execution.vulnerabilities),
    searchTextFilter
  );
  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }

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
                customSearch={{
                  customSearchDefault: searchTextFilter,
                  isCustomSearchEnabled: true,
                  onUpdateCustomSearch: onSearchTextChange,
                  position: "right",
                }}
                dataset={filterSearchtextResult}
                exportCsv={false}
                headers={headersCompromisedToeTable}
                id={"tblCompromisedToe"}
                isFilterEnabled={isFilterEnabled}
                onUpdateEnableFilter={handleUpdateFilter}
                pageSize={100}
                search={false}
              />
            </Route>
            <Route path={"/log"}>
              <SyntaxHighlighter
                language={"text"}
                // eslint-disable-next-line react/forbid-component-props
                style={monokaiSublime}
                wrapLines={true}
              >
                {execution.log}
              </SyntaxHighlighter>
            </Route>
          </Switch>
        </TabContent>
      </MemoryRouter>
    </div>
  );
};

export { Execution };
