/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for the sake of readability
 */

// Third parties imports
import { QueryResult } from "@apollo/react-common";
import { Query } from "@apollo/react-components";
import _ from "lodash";
import React from "react";
import { dateFilter, selectFilter } from "react-bootstrap-table2-filter";
import { useParams } from "react-router-dom";

// Local imports
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { statusFormatter } from "components/DataTableNext/formatters";
import { IHeaderConfig } from "components/DataTableNext/types";
import { Modal } from "components/Modal";
import { Execution } from "scenes/Dashboard/containers/ProjectForcesView/execution";
import { GET_FORCES_EXECUTIONS } from "scenes/Dashboard/containers/ProjectForcesView/queries";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

export interface IExploitResult {
  exploitability: number;
  kind: string;
  state: string;
  where: string;
  who: string;
}
export interface IFoundVulnerabilities {
  accepted: number;
  closed: number;
  open: number;
  total: number;
}

export interface IVulnerabilities {
  accepted: IExploitResult[];
  closed: IExploitResult[];
  numOfAcceptedVulnerabilities: number;
  numOfClosedVulnerabilities: number;
  numOfOpenVulnerabilities: number;
  open: IExploitResult[];
}

export interface IExecution {
  date: string;
  execution_id: string;
  exitCode: string;
  foundVulnerabilities: IFoundVulnerabilities;
  gitRepo: string;
  kind: string;
  log?: string;
  projectName?: string;
  status: string;
  strictness: string;
  vulnerabilities: IVulnerabilities;
}

const projectForcesView: React.FC = (): JSX.Element => {
  const { projectName } = useParams<{ projectName: string }>();

  // States
  const defaultCurrentRow: IExecution = {
    date: "",
    execution_id: "",
    exitCode: "",
    foundVulnerabilities: {
      accepted: 0,
      closed: 0,
      open: 0,
      total: 0,
    },
    gitRepo: "",
    kind: "",
    log: "",
    status: "",
    strictness: "",
    vulnerabilities: {
      accepted: [],
      closed: [],
      numOfAcceptedVulnerabilities: 0,
      numOfClosedVulnerabilities: 0,
      numOfOpenVulnerabilities: 0,
      open: [],
    },
  };

  const selectOptionsKind: optionSelectFilterProps[] = [
    { value: "ALL", label: "ALL" },
    { value: "DAST", label: "DAST" },
    { value: "SAST", label: "SAST" },
  ];
  const selectOptionsStatus: optionSelectFilterProps[] = [
    { value: "Vulnerable", label: "Vulnerable" },
    { value: "Secure", label: "Secure" },
  ];
  const selectOptionsStrictness: optionSelectFilterProps[] = [
    { value: "Tolerant", label: "Tolerant" },
    { value: "Strict", label: "Strict" },
  ];

  const [isFilterEnabled, setFilterEnabled] = useStoredState<boolean>("forcesExecutionFilters", false);

  const [currentRow, updateRow] = React.useState(defaultCurrentRow);
  const [isExecutionDetailsModalOpen, setExecutionDetailsModalOpen] = React.useState(false);

  const handleUpdateFilter: () => void = (): void => {
    setFilterEnabled(!isFilterEnabled);
  };

  const onFilterKind: ((filterVal: string) => void) = (filterVal: string): void => {
    sessionStorage.setItem("kindForcesFilter", filterVal);
  };
  const onFilterStatus: ((filterVal: string) => void) = (filterVal: string): void => {
    sessionStorage.setItem("statusForcesFilter", filterVal);
  };
  const onStrictnessStatus: ((filterVal: string) => void) = (filterVal: string): void => {
    sessionStorage.setItem("strictnessForcesFilter", filterVal);
  };
  const onSortState: ((dataField: string, order: SortOrder) => void) = (
    dataField: string, order: SortOrder,
  ): void => {
    const newSorted: Sorted = { dataField, order };
    sessionStorage.setItem("forcesSort", JSON.stringify(newSorted));
  };

  const toTitleCase: ((str: string) => string) = (str: string): string =>
    str.split(" ")
      .map((w: string): string => w[0].toUpperCase() + w.substr(1)
        .toLowerCase())
      .join(" ");

  const formatDate: ((date: string) => string) = (date: string): string => {
    const dateObj: Date = new Date(date);

    const toStringAndPad: ((input: number, positions: number) => string) =
      (input: number, positions: number): string => input.toString()
        .padStart(positions, "0");

    const year: string = toStringAndPad(dateObj.getFullYear(), 4);
    // Warning: months are 0 indexed: January is 0, December is 11
    const month: string = toStringAndPad(dateObj.getMonth() + 1, 2);
    // Warning: Date.getDay() returns the day of the week: Monday is 1, Friday is 5
    const day: string = toStringAndPad(dateObj.getDate(), 2);
    const hours: string = toStringAndPad(dateObj.getHours(), 2);
    const minutes: string = toStringAndPad(dateObj.getMinutes(), 2);

    return `${year}-${month}-${day} ${hours}:${minutes}`;
  };

  const headersExecutionTable: IHeaderConfig[] = [
    {
      align: "center", dataField: "date", filter: dateFilter(),
      header: translate.t("group.forces.date"), onSort: onSortState,
    },
    {
      align: "center", dataField: "status", filter: selectFilter({
        defaultValue: _.get(sessionStorage, "statusForcesFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: statusFormatter,
      header: translate.t("group.forces.status.title"), onSort: onSortState, wrapped: true,
    },
    {
      align: "center", dataField: "foundVulnerabilities.total",
      header: translate.t("group.forces.status.vulnerabilities"),
      onSort: onSortState, wrapped: true,
    },
    {
      align: "center", dataField: "strictness", filter: selectFilter({
        defaultValue: _.get(sessionStorage, "strictnessForcesFilter"),
        onFilter: onStrictnessStatus,
        options: selectOptionsStrictness,
      }),
      header: translate.t("group.forces.strictness.title"),
      onSort: onSortState, wrapped: true,
    },
    {
      align: "center", dataField: "kind", filter: selectFilter({
        defaultValue: _.get(sessionStorage, "kindForcesFilter"),
        onFilter: onFilterKind,
        options: selectOptionsKind,
      }),
      header: translate.t("group.forces.kind.title"),
      onSort: onSortState,  wrapped: true,
    },
    {
      align: "center", dataField: "gitRepo", header: translate.t("group.forces.git_repo"),
      onSort: onSortState, wrapped: true,
    },
    {
      align: "center", dataField: "execution_id", header: translate.t("group.forces.identifier"),
      onSort: onSortState, wrapped: true,
    },
  ];

  const openSeeExecutionDetailsModal: ((event: object, row: IExecution) => void) = (
    _0: object, row: IExecution,
  ): void => {
    updateRow(row);
    setExecutionDetailsModalOpen(true);
  };

  const closeSeeExecutionDetailsModal: (() => void) = (): void => {
    setExecutionDetailsModalOpen(false);
  };

  const handleQryErrors: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning("An error occurred getting executions", error);
    });
  };

  return (
    <Query
      query={GET_FORCES_EXECUTIONS}
      variables={{ projectName }}
      onError={handleQryErrors}
    >
      {
        ({ data }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) {
            return <React.Fragment />;
          }

          const executions: IExecution[] = data.forcesExecutions.executions
            .map((execution: IExecution) => {
              const date: string = formatDate(execution.date);
              const kind: string =
                translate.t(`group.forces.kind.${execution.kind}`);
              const strictness: string = toTitleCase(
                translate.t(
                  execution.strictness === "lax"
                    ? "group.forces.strictness.tolerant"
                    : "group.forces.strictness.strict"));
              const vulnerabilities: IVulnerabilities =
                execution.vulnerabilities;
              const foundVulnerabilities: IFoundVulnerabilities = {
                    accepted: vulnerabilities.numOfAcceptedVulnerabilities,
                    closed: vulnerabilities.numOfClosedVulnerabilities,
                    open: vulnerabilities.numOfOpenVulnerabilities,
                    total:
                      vulnerabilities.numOfAcceptedVulnerabilities +
                      vulnerabilities.numOfOpenVulnerabilities +
                      vulnerabilities.numOfClosedVulnerabilities,
                  };
              const status: string = translate.t(
                foundVulnerabilities.open === 0
                  ? "group.forces.status.secure"
                  : "group.forces.status.vulnerable");

              return {
                ...execution,
                date,
                foundVulnerabilities,
                kind,
                status,
                strictness,
              };
            });

          const initialSort: string = JSON.stringify({ dataField: "date", order: "desc" });

          return (
              <React.StrictMode>
                <p>{translate.t("group.forces.table_advice")}</p>
                <DataTableNext
                  bordered={true}
                  dataset={executions}
                  defaultSorted={JSON.parse(_.get(sessionStorage, "forcesSort", initialSort))}
                  exportCsv={true}
                  search={true}
                  headers={headersExecutionTable}
                  id="tblForcesExecutions"
                  pageSize={100}
                  rowEvents={{ onClick: openSeeExecutionDetailsModal }}
                  isFilterEnabled={isFilterEnabled}
                  onUpdateEnableFilter={handleUpdateFilter}
                />
                <Modal
                  headerTitle={translate.t("group.forces.execution_details_modal.title")}
                  open={isExecutionDetailsModalOpen}
                  size={"largeModal"}
                >
                  <Execution {...currentRow} />
                  <hr />
                  <Row>
                    <Col100>
                      <ButtonToolbar>
                        <Button onClick={closeSeeExecutionDetailsModal}>
                          {translate.t("group.forces.execution_details_modal.close")}
                        </Button>
                      </ButtonToolbar>
                    </Col100>
                  </Row>
                </Modal>
              </React.StrictMode>
            );
        }}
    </Query>
  );
};

export { projectForcesView as ProjectForcesView };
