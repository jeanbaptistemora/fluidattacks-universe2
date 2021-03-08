/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for the sake of readability
 */

// Third parties imports
import { useQuery } from "@apollo/react-hooks";
import _ from "lodash";
import React, { ReactElement } from "react";
import { selectFilter } from "react-bootstrap-table2-filter";
import { MemoryRouter, Route } from "react-router";
// tslint:disable-next-line no-submodule-imports
import SyntaxHighlighter from "react-syntax-highlighter/dist/esm/light";
// tslint:disable-next-line no-submodule-imports
import { default as monokaiSublime } from "react-syntax-highlighter/dist/esm/styles/hljs/monokai-sublime";

import { DataTableNext } from "components/DataTableNext";
import { statusFormatter } from "components/DataTableNext/formatters";
import { IHeaderConfig } from "components/DataTableNext/types";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import {
  IExecution,
  IExploitResult,
  IFoundVulnerabilities,
  IVulnerabilities,
} from "scenes/Dashboard/containers/ProjectForcesView";
import styles from "scenes/Dashboard/containers/ProjectForcesView/index.css";
import { GET_FORCES_EXECUTION } from "scenes/Dashboard/containers/ProjectForcesView/queries";
import { Col33, Row, TabsContainer } from "styles/styledComponents";
import { useStoredState } from "utils/hooks";
import { translate } from "utils/translations/translate";

const modalExecution: React.FC<IExecution> = (
  props: Readonly<IExecution>,
): JSX.Element => {
  const isOld: boolean = props.log !== undefined;

  const [isFilterEnabled, setFilterEnabled] = useStoredState<boolean>("forcesExecutionFilters", false);

  const { loading, data } = useQuery(GET_FORCES_EXECUTION, {
    skip: isOld,
    variables: {
      executionId: props.execution_id,
      projectName: props.projectName,
    },
  });
  if (loading && !isOld) {

    return <p>Loading ...</p>;
  }

  const selectOptionsStatus: optionSelectFilterProps[] = [
    { value: "Vulnerable", label: "Vulnerable" },
    { value: "Secure", label: "Secure" },
  ];
  const selectOptionsKind: optionSelectFilterProps[] = [
    { value: "DAST", label: "DAST" },
    { value: "SAST", label: "SAST" },
  ];
  const selectOptionsExploitability: optionSelectFilterProps[] = [
    { value: "Unproven", label: "Unproven" },
    { value: "Proof of concept", label: "Proof of concept" },
    { value: "Functional", label: "Functional" },
    { value: "High", label: "High" },
  ];

  const execution: IExecution = isOld ? props : { ...props, ...data.forcesExecution };

  const handleUpdateFilter: () => void = (): void => {
    setFilterEnabled(!isFilterEnabled);
  };
  const onFilterStatus: ((filterVal: string) => void) = (filterVal: string): void => {
    sessionStorage.setItem("statusExecutionFilter", filterVal);
  };
  const onFilterKind: ((filterVal: string) => void) = (filterVal: string): void => {
    sessionStorage.setItem("kindExecutionFilter", filterVal);
  };
  const onFilterExploitability: ((filterVal: string) => void) = (filterVal: string): void => {
    sessionStorage.setItem("exploitabilityForcesFilter", filterVal);
  };
  const formatText: ((text: string) => ReactElement<Text>) = (text: string): ReactElement<Text> =>
    <p className={styles.wrapped}>{text}</p>;

  const stateResolve: (status: string) => string = (status: string): string => {
    switch (status) {
      case "OPEN":
        return translate.t("group.forces.status.vulnerable");
      case "CLOSED":
        return translate.t("group.forces.status.secure");
      case "ACCEPTED":
        return translate.t("group.forces.status.accepted");
      default:
        return "";
    }
  };

  const getVulnerabilitySummaries: (
    foundVulnerabilities: IFoundVulnerabilities,
  ) => string = (
    foundVulnerabilities: IFoundVulnerabilities,
    ): string => {
        const openTrans: string = translate.t(
          "group.forces.foundVulnerabilitiesNew.open");
        const acceptedTrans: string = translate.t(
          "group.forces.foundVulnerabilitiesNew.accepted");
        const closedTrans: string = translate.t(
          "group.forces.foundVulnerabilitiesNew.closed");
        const totalTrans: string = translate.t(
          "group.forces.foundVulnerabilitiesNew.total");

        const openStr: string = `${foundVulnerabilities.open} ${openTrans}`;
        const acceptedStr: string = `${foundVulnerabilities.accepted} ${acceptedTrans}`;
        const closedStr: string = `${foundVulnerabilities.closed} ${closedTrans}`;
        const totalStr: string = `${foundVulnerabilities.total} ${totalTrans}`;

        return `${openStr}, ${acceptedStr}, ${closedStr}, ${totalStr}`;
    };

  const getDatasetFromVulnerabilities: (
    vulnerabilities: IVulnerabilities,
  ) => Dictionary[] = (
    vulnerabilities: IVulnerabilities,
    ): Dictionary[] => {
      const vulns: IExploitResult[] = vulnerabilities.open.concat(
            vulnerabilities.closed.concat(vulnerabilities.accepted),
        );

      return vulns.map((elem: IExploitResult) => ({
        ...elem,
        state: stateResolve(elem.state),
      }));
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
          header: translate.t("group.forces.compromisedToe.exploitability"),
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
          header: translate.t("group.forces.compromisedToe.status"),
          width: "10%",
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
          header: translate.t("group.forces.compromisedToe.type"),
          width: "10%",
          wrapped: true,
        },
        {
          dataField: "who",
          formatter: formatText,
          header: translate.t("group.forces.compromisedToe.what"),
          wrapped: true,
        },
        {
          dataField: "where",
          formatter: formatText,
          header: translate.t("group.forces.compromisedToe.where"),
          wrapped: true,
        },
      ];

  return (
    <div>
      <Row className={"nb3"}>
        <Col33><p><b>{translate.t("group.forces.date")}</b></p></Col33>
        <Col33><p>{execution.date}</p></Col33>
      </Row>
      <Row className={"nb3"}>
        <Col33><p><b>{translate.t("group.forces.status.title")}</b></p></Col33>
        <Col33><p>{execution.status}</p></Col33>
      </Row>
      <Row className={"nb3"}>
        <Col33><p><b>{translate.t("group.forces.strictness.title")}</b></p></Col33>
        <Col33><p>{execution.strictness}</p></Col33>
      </Row>
      <Row className={"nb3"}>
        <Col33><p><b>{translate.t("group.forces.kind.title")}</b></p></Col33>
        <Col33><p>{execution.kind}</p></Col33>
      </Row>
      <Row className={"nb3"}>
        <Col33><p><b>{translate.t("group.forces.gitRepo")}</b></p></Col33>
        <Col33><p>{execution.gitRepo}</p></Col33>
      </Row>
      <Row className={"nb3"}>
        <Col33><p><b>{translate.t("group.forces.identifier")}</b></p></Col33>
        <Col33><p>{execution.execution_id}</p></Col33>
      </Row>
      <Row className={"nb3"}>
        <Col33><p><b>{translate.t("group.forces.foundVulnerabilities.title")}</b></p></Col33>
        <Col33>
          <p className={styles.wrapped}>
            {getVulnerabilitySummaries(execution.foundVulnerabilities)}
          </p>
        </Col33>
      </Row>
      <br/>
      <MemoryRouter
        initialEntries={["/summary", "/log"]}
        initialIndex={0}
      >
        <TabsContainer>
          <ContentTab
            icon="icon pe-7s-graph3"
            id="forcesExecutionSummaryTab"
            link="/summary"
            title={translate.t("group.forces.tabs.summary.text")}
            tooltip={translate.t("group.forces.tabs.summary.tooltip")}/>
          <ContentTab
            icon="icon pe-7s-file"
            id="forcesExecutionLogTab"
            link="/log"
            title={translate.t("group.forces.tabs.log.text")}
            tooltip={translate.t("group.forces.tabs.log.tooltip")}/>
        </TabsContainer>
        <br />
        <Route path="/summary">
          <DataTableNext
            bordered={true}
            dataset={getDatasetFromVulnerabilities(execution.vulnerabilities)}
            exportCsv={false}
            search={true}
            headers={headersCompromisedToeTable}
            id="tblCompromisedToe"
            pageSize={100}
            columnToggle={true}
            isFilterEnabled={isFilterEnabled}
            onUpdateEnableFilter={handleUpdateFilter}
          />
        </Route>
        <Route path="/log">
          <SyntaxHighlighter style={monokaiSublime} language="yaml" wrapLines={true}>
            {execution.log}
          </SyntaxHighlighter>
        </Route>
      </MemoryRouter>
    </div>
  );
};

export { modalExecution as Execution };
