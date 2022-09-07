/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type {
  ColumnDef,
  ColumnFiltersState,
  PaginationState,
  Row,
  SortingState,
} from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import type { FormEvent } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Modal } from "components/Modal";
import { Table } from "components/TableNew";
import type { ICellHelper } from "components/TableNew/types";
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

const GroupForcesView: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
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

  const [currentRow, setCurrentRow] = useState(defaultCurrentRow);
  const [isExecutionDetailsModalOpen, setIsExecutionDetailsModalOpen] =
    useState(false);
  const [columnFilters, setColumnFilters] = useStoredState<ColumnFiltersState>(
    "tblForcesExecutionsTableFilters",
    []
  );
  const [sorting, setSorting] = useStoredState<SortingState>(
    "tblForcesExecutionsSorting",
    []
  );
  const [pagination, setPagination] = useStoredState<PaginationState>(
    "tblForcesExecutionsPagination",
    {
      pageIndex: 0,
      pageSize: 10,
    }
  );

  const toTitleCase: (str: string) => string = (str: string): string =>
    str
      .split(" ")
      .map(
        (item: string): string =>
          item[0].toUpperCase() + item.substr(1).toLowerCase()
      )
      .join(" ");

  const headersExecutionTable: ColumnDef<IExecution>[] = [
    {
      accessorKey: "date",
      header: t("group.forces.date"),
      meta: { filterType: "dateRange" },
    },
    {
      accessorKey: "status",
      cell: (cell: ICellHelper<IExecution>): JSX.Element =>
        statusFormatter(cell.getValue()),
      header: t("group.forces.status.title"),
      meta: { filterType: "select" },
    },
    {
      accessorFn: (row: IExecution): number => {
        return row.foundVulnerabilities.total;
      },
      header: String(t("group.forces.status.vulnerabilities")),
      meta: { filterType: "number" },
    },
    {
      accessorKey: "strictness",
      header: t("group.forces.strictness.title"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "kind",
      header: t("group.forces.kind.title"),
    },
    {
      accessorKey: "gitRepo",
      header: t("group.forces.gitRepo"),
    },
    {
      accessorKey: "executionId",
      header: t("group.forces.identifier"),
    },
  ];

  function openSeeExecutionDetailsModal(
    rowInfo: Row<IExecution>
  ): (event: FormEvent) => void {
    return (event: FormEvent): void => {
      setCurrentRow(rowInfo.original);
      setIsExecutionDetailsModalOpen(true);
      event.preventDefault();
    };
  }

  const closeSeeExecutionDetailsModal: () => void = useCallback((): void => {
    setIsExecutionDetailsModalOpen(false);
  }, []);

  const handleQryErrors: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(t("groupAlerts.errorTextsad"));
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
      const kind: string = t(`group.forces.kind.${execution.kind}`);
      const strictness: string = toTitleCase(
        t(
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
      const status: string = t(
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

  return (
    <React.StrictMode>
      <p>{t("group.forces.tableAdvice")}</p>
      <Table
        columnFilterSetter={setColumnFilters}
        columnFilterState={columnFilters}
        columns={headersExecutionTable}
        data={executions}
        enableColumnFilters={true}
        exportCsv={true}
        id={"tblForcesExecutions"}
        onRowClick={openSeeExecutionDetailsModal}
        paginationSetter={setPagination}
        paginationState={pagination}
        sortingSetter={setSorting}
        sortingState={sorting}
      />
      <Modal
        onClose={closeSeeExecutionDetailsModal}
        open={isExecutionDetailsModalOpen}
        title={t("group.forces.executionDetailsModal.title")}
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
      </Modal>
    </React.StrictMode>
  );
};

export { GroupForcesView };
