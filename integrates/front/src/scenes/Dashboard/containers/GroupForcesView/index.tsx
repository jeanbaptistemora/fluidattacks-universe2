import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { useParams } from "react-router-dom";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { Table } from "components/Table";
import type { IFilterProps, IHeaderConfig } from "components/Table/types";
import {
  filterDateRange,
  filterSearchText,
  filterSelect,
  filterText,
} from "components/Table/utils";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { Execution } from "scenes/Dashboard/containers/GroupForcesView/execution";
import { GET_FORCES_EXECUTIONS } from "scenes/Dashboard/containers/GroupForcesView/queries";
import type {
  IExecution,
  IFoundVulnerabilities,
  IGetExecution,
} from "scenes/Dashboard/containers/GroupForcesView/types";
import { formatDate } from "utils/formatHelpers";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IFilterSet {
  dateRange: { max: string; min: string };
  repository: string;
  status: string;
  strictness: string;
  type: string;
}

const GroupForcesView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();

  // States
  const defaultCurrentRow: IExecution = {
    date: "",
    executionId: "",
    exitCode: "",
    foundVulnerabilities: {
      accepted: 0,
      closed: 0,
      open: 0,
      total: 0,
    },
    gitRepo: "",
    gracePeriod: 0,
    kind: "",
    log: "",
    severityThreshold: 0,
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

  const [currentRow, updateRow] = useState(defaultCurrentRow);
  const [isExecutionDetailsModalOpen, setExecutionDetailsModalOpen] =
    useState(false);

  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("groupForcesCustomFilters", false);

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [filterGroupForcesTable, setFilterGroupForcesTable] =
    useStoredState<IFilterSet>(
      "filterGroupForcesSet",
      {
        dateRange: { max: "", min: "" },
        repository: "",
        status: "",
        strictness: "",
        type: "",
      },
      localStorage
    );

  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

  const onSortState: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted = { dataField, order };
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

  const headersExecutionTable: IHeaderConfig[] = [
    {
      dataField: "date",
      header: translate.t("group.forces.date"),
      onSort: onSortState,
    },
    {
      dataField: "status",
      formatter: statusFormatter,
      header: translate.t("group.forces.status.title"),
      onSort: onSortState,
      width: "105px",
      wrapped: true,
    },
    {
      dataField: "foundVulnerabilities.total",
      header: translate.t("group.forces.status.vulnerabilities"),
      onSort: onSortState,
      wrapped: true,
    },
    {
      dataField: "strictness",
      header: translate.t("group.forces.strictness.title"),
      onSort: onSortState,
      wrapped: true,
    },
    {
      dataField: "kind",
      header: translate.t("group.forces.kind.title"),
      onSort: onSortState,
      wrapped: true,
    },
    {
      dataField: "gitRepo",
      header: translate.t("group.forces.gitRepo"),
      onSort: onSortState,
      wrapped: true,
    },
    {
      dataField: "executionId",
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

  const closeSeeExecutionDetailsModal: () => void = useCallback((): void => {
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

  const { data } = useQuery<IGetExecution>(GET_FORCES_EXECUTIONS, {
    onError: handleQryErrors,
    variables: { groupName },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

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
      const foundVulnerabilities: IFoundVulnerabilities = _.isNull(
        vulnerabilities
      )
        ? {
            accepted: 0,
            closed: 0,
            open: 0,
            total: 0,
          }
        : {
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

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchTextExecutions: IExecution[] = filterSearchText(
    executions,
    searchTextFilter
  );

  function onDateMaxChange(event: React.ChangeEvent<HTMLInputElement>): void {
    event.persist();
    setFilterGroupForcesTable(
      (value): IFilterSet => ({
        ...value,
        dateRange: { ...value.dateRange, max: event.currentTarget.value },
      })
    );
  }
  function onDateMinChange(event: React.ChangeEvent<HTMLInputElement>): void {
    event.persist();
    setFilterGroupForcesTable(
      (value): IFilterSet => ({
        ...value,
        dateRange: { ...value.dateRange, min: event.currentTarget.value },
      })
    );
  }
  const filterDateRangeExecutions: IExecution[] = filterDateRange(
    executions,
    filterGroupForcesTable.dateRange,
    "date"
  );

  function onStatusChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterGroupForcesTable(
      (value): IFilterSet => ({
        ...value,
        status: event.target.value,
      })
    );
  }
  const filterStatusExecutions: IExecution[] = filterSelect(
    executions,
    filterGroupForcesTable.status,
    "status"
  );

  function onStrictnessChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    event.persist();
    setFilterGroupForcesTable(
      (value): IFilterSet => ({
        ...value,
        strictness: event.target.value,
      })
    );
  }
  const filterStrictnessExecutions: IExecution[] = filterSelect(
    executions,
    filterGroupForcesTable.strictness,
    "strictness"
  );

  function onTypeChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterGroupForcesTable(
      (value): IFilterSet => ({
        ...value,
        type: event.target.value,
      })
    );
  }
  const filterTypeExecutions: IExecution[] = filterSelect(
    executions,
    filterGroupForcesTable.type,
    "kind"
  );

  function onRepositoryChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterGroupForcesTable(
      (value): IFilterSet => ({
        ...value,
        repository: event.target.value,
      })
    );
  }
  const filterGroupNameExecutions: IExecution[] = filterText(
    executions,
    filterGroupForcesTable.repository,
    "gitRepo"
  );

  function clearFilters(): void {
    setFilterGroupForcesTable(
      (): IFilterSet => ({
        dateRange: { max: "", min: "" },
        repository: "",
        status: "",
        strictness: "",
        type: "",
      })
    );
    setSearchTextFilter("");
  }

  const resultExecutions: IExecution[] = _.intersection(
    filterSearchTextExecutions,
    filterDateRangeExecutions,
    filterStatusExecutions,
    filterStrictnessExecutions,
    filterTypeExecutions,
    filterGroupNameExecutions
  );

  const customFiltersProps: IFilterProps[] = [
    {
      defaultValue: "",
      placeholder: "Date (Range)",
      rangeProps: {
        defaultValue: filterGroupForcesTable.dateRange,
        onChangeMax: onDateMaxChange,
        onChangeMin: onDateMinChange,
      },
      tooltipId: "group.forces.filtersTooltips.date.id",
      tooltipMessage: "group.forces.filtersTooltips.date",
      type: "dateRange",
    },
    {
      defaultValue: filterGroupForcesTable.status,
      onChangeSelect: onStatusChange,
      placeholder: "Status",
      selectOptions: {
        Secure: "Secure",
        Vulnerable: "Vulnerable",
      },
      tooltipId: "group.forces.filtersTooltips.status.id",
      tooltipMessage: "group.forces.filtersTooltips.status",
      type: "select",
    },
    {
      defaultValue: filterGroupForcesTable.strictness,
      onChangeSelect: onStrictnessChange,
      placeholder: "Strictness",
      selectOptions: {
        Strict: "Strict",
        Tolerant: "Tolerant",
      },
      tooltipId: "group.forces.filtersTooltips.strictness.id",
      tooltipMessage: "group.forces.filtersTooltips.strictness",
      type: "select",
    },
    {
      defaultValue: filterGroupForcesTable.type,
      onChangeSelect: onTypeChange,
      placeholder: "Type",
      selectOptions: {
        ALL: "ALL",
        DAST: "DAST",
        SAST: "SAST",
      },
      tooltipId: "group.forces.filtersTooltips.kind.id",
      tooltipMessage: "group.forces.filtersTooltips.kind",
      type: "select",
    },
    {
      defaultValue: filterGroupForcesTable.repository,
      onChangeInput: onRepositoryChange,
      placeholder: "Git Repository",
      tooltipId: "group.forces.filtersTooltips.repository.id",
      tooltipMessage: "group.forces.filtersTooltips.repository",
      type: "text",
    },
  ];

  return (
    <React.StrictMode>
      <p>{translate.t("group.forces.tableAdvice")}</p>
      <Table
        clearFiltersButton={clearFilters}
        customFilters={{
          customFiltersProps,
          isCustomFilterEnabled,
          onUpdateEnableCustomFilter: handleUpdateCustomFilter,
          oneRowMessage: true,
          resultSize: {
            current: resultExecutions.length,
            total: executions.length,
          },
        }}
        customSearch={{
          customSearchDefault: searchTextFilter,
          isCustomSearchEnabled: true,
          onUpdateCustomSearch: onSearchTextChange,
          position: "right",
        }}
        dataset={resultExecutions}
        defaultSorted={JSON.parse(
          _.get(sessionStorage, "forcesSort", initialSort)
        )}
        exportCsv={true}
        headers={headersExecutionTable}
        id={"tblForcesExecutions"}
        pageSize={100}
        rowEvents={{ onClick: openSeeExecutionDetailsModal }}
        search={false}
      />
      <Modal
        onClose={closeSeeExecutionDetailsModal}
        open={isExecutionDetailsModalOpen}
        title={translate.t("group.forces.executionDetailsModal.title")}
      >
        <Execution
          date={currentRow.date}
          executionId={currentRow.executionId}
          exitCode={currentRow.exitCode}
          foundVulnerabilities={currentRow.foundVulnerabilities}
          gitRepo={currentRow.gitRepo}
          gracePeriod={currentRow.gracePeriod}
          groupName={currentRow.groupName}
          kind={currentRow.kind}
          log={currentRow.log}
          severityThreshold={currentRow.severityThreshold}
          status={currentRow.status}
          strictness={currentRow.strictness}
          vulnerabilities={currentRow.vulnerabilities}
        />
        <div>
          <div>
            <ModalFooter>
              <Button
                onClick={closeSeeExecutionDetailsModal}
                variant={"secondary"}
              >
                {translate.t("group.forces.executionDetailsModal.close")}
              </Button>
            </ModalFooter>
          </div>
        </div>
      </Modal>
    </React.StrictMode>
  );
};

export { GroupForcesView };
