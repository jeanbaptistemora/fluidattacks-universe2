import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { Execution } from "scenes/Dashboard/containers/ProjectForcesView/execution";
import { GET_FORCES_EXECUTIONS } from "scenes/Dashboard/containers/ProjectForcesView/queries";
import type { GraphQLError } from "graphql";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Logger } from "utils/logger";
import { Modal } from "components/Modal";
import React from "react";
import _ from "lodash";
import { msgError } from "utils/notifications";
import { statusFormatter } from "components/DataTableNext/formatters";
import { translate } from "utils/translations/translate";
import { useParams } from "react-router-dom";
import { useQuery } from "@apollo/react-hooks";
import { useStoredState } from "utils/hooks";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import type {
  IExecution,
  IFoundVulnerabilities,
} from "scenes/Dashboard/containers/ProjectForcesView/types";
import { dateFilter, selectFilter } from "react-bootstrap-table2-filter";

const ProjectForcesView: React.FC = (): JSX.Element => {
  const { projectName } = useParams<{ projectName: string }>();

  // States
  const defaultCurrentRow: IExecution = {
    date: "",
    // eslint-disable-next-line camelcase -- API related
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
    { label: "ALL", value: "ALL" },
    { label: "DAST", value: "DAST" },
    { label: "SAST", value: "SAST" },
  ];
  const selectOptionsStatus: optionSelectFilterProps[] = [
    { label: "Vulnerable", value: "Vulnerable" },
    { label: "Secure", value: "Secure" },
  ];
  const selectOptionsStrictness: optionSelectFilterProps[] = [
    { label: "Tolerant", value: "Tolerant" },
    { label: "Strict", value: "Strict" },
  ];

  const [isFilterEnabled, setFilterEnabled] = useStoredState<boolean>(
    "forcesExecutionFilters",
    false
  );

  const [currentRow, updateRow] = React.useState(defaultCurrentRow);
  const [
    isExecutionDetailsModalOpen,
    setExecutionDetailsModalOpen,
  ] = React.useState(false);

  const handleUpdateFilter: () => void = React.useCallback((): void => {
    setFilterEnabled(!isFilterEnabled);
  }, [isFilterEnabled, setFilterEnabled]);

  const onFilterKind: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("kindForcesFilter", filterVal);
  };
  const onFilterStatus: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("statusForcesFilter", filterVal);
  };
  const onStrictnessStatus: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("strictnessForcesFilter", filterVal);
  };
  const onSortState: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted: Sorted = { dataField, order };
    sessionStorage.setItem("forcesSort", JSON.stringify(newSorted));
  };

  const toTitleCase: (str: string) => string = (str: string): string =>
    str
      .split(" ")
      .map(
        (item: string): string =>
          item[0].toUpperCase() + item.substr(1).toLowerCase()
      )
      .join(" ");

  const formatDate: (date: string) => string = (date: string): string => {
    const dateObj: Date = new Date(date);

    const toStringAndPad: (input: number, positions: number) => string = (
      input: number,
      positions: number
    ): string => input.toString().padStart(positions, "0");

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
      align: "center",
      dataField: "date",
      filter: dateFilter(),
      header: translate.t("group.forces.date"),
      onSort: onSortState,
    },
    {
      align: "center",
      dataField: "status",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "statusForcesFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: statusFormatter,
      header: translate.t("group.forces.status.title"),
      onSort: onSortState,
      wrapped: true,
    },
    {
      align: "center",
      dataField: "foundVulnerabilities.total",
      header: translate.t("group.forces.status.vulnerabilities"),
      onSort: onSortState,
      wrapped: true,
    },
    {
      align: "center",
      dataField: "strictness",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "strictnessForcesFilter"),
        onFilter: onStrictnessStatus,
        options: selectOptionsStrictness,
      }),
      header: translate.t("group.forces.strictness.title"),
      onSort: onSortState,
      wrapped: true,
    },
    {
      align: "center",
      dataField: "kind",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "kindForcesFilter"),
        onFilter: onFilterKind,
        options: selectOptionsKind,
      }),
      header: translate.t("group.forces.kind.title"),
      onSort: onSortState,
      wrapped: true,
    },
    {
      align: "center",
      dataField: "gitRepo",
      header: translate.t("group.forces.gitRepo"),
      onSort: onSortState,
      wrapped: true,
    },
    {
      align: "center",
      dataField: "execution_id",
      header: translate.t("group.forces.identifier"),
      onSort: onSortState,
      wrapped: true,
    },
  ];

  const openSeeExecutionDetailsModal: (
    event: Record<string, unknown>,
    row: IExecution
  ) => void = (_0: Record<string, unknown>, row: IExecution): void => {
    updateRow(row);
    setExecutionDetailsModalOpen(true);
  };

  const closeSeeExecutionDetailsModal: () => void = React.useCallback((): void => {
    setExecutionDetailsModalOpen(false);
  }, []);

  const handleQryErrors: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred getting executions", error);
    });
  };

  const { data } = useQuery(GET_FORCES_EXECUTIONS, {
    onError: handleQryErrors,
    variables: { projectName },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
  const executions: IExecution[] = data.forcesExecutions.executions.map(
    (execution: IExecution): IExecution => {
      const date: string = formatDate(execution.date);
      const kind: string = translate.t(`group.forces.kind.${execution.kind}`);
      const strictness: string = toTitleCase(
        translate.t(
          execution.strictness === "lax"
            ? "group.forces.strictness.tolerant"
            : "group.forces.strictness.strict"
        )
      );
      const { vulnerabilities } = execution;
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
          : "group.forces.status.vulnerable"
      );

      return {
        ...execution,
        date,
        foundVulnerabilities,
        kind,
        status,
        strictness,
      };
    }
  );

  const initialSort: string = JSON.stringify({
    dataField: "date",
    order: "desc",
  });

  return (
    <React.StrictMode>
      <p>{translate.t("group.forces.tableAdvice")}</p>
      <DataTableNext
        bordered={true}
        dataset={executions}
        defaultSorted={JSON.parse(
          _.get(sessionStorage, "forcesSort", initialSort)
        )}
        exportCsv={true}
        headers={headersExecutionTable}
        id={"tblForcesExecutions"}
        isFilterEnabled={isFilterEnabled}
        onUpdateEnableFilter={handleUpdateFilter}
        pageSize={100}
        rowEvents={{ onClick: openSeeExecutionDetailsModal }}
        search={true}
      />
      <Modal
        headerTitle={translate.t("group.forces.executionDetailsModal.title")}
        open={isExecutionDetailsModalOpen}
        size={"largeModal"}
      >
        {/* eslint-disable-next-line react/jsx-props-no-spreading -- Preferred for readability */}
        <Execution
          date={currentRow.date}
          execution_id={currentRow.execution_id}
          exitCode={currentRow.exitCode}
          foundVulnerabilities={currentRow.foundVulnerabilities}
          gitRepo={currentRow.gitRepo}
          kind={currentRow.kind}
          log={currentRow.log}
          projectName={currentRow.projectName}
          status={currentRow.status}
          strictness={currentRow.strictness}
          vulnerabilities={currentRow.vulnerabilities}
        />
        <hr />
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button onClick={closeSeeExecutionDetailsModal}>
                {translate.t("group.forces.executionDetailsModal.close")}
              </Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      </Modal>
    </React.StrictMode>
  );
};

export { ProjectForcesView };
