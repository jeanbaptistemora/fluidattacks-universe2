/* eslint-disable react/jsx-props-no-spreading */
import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { ColumnDef, Row, SortingState } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useMemo, useState } from "react";
import type { FormEvent } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { formatExecutions } from "./utils";

import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Modal } from "components/Modal";
import { Table } from "components/Table";
import { filterDate } from "components/Table/filters/filterFunctions/filterDate";
import type { ICellHelper } from "components/Table/types";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { Execution } from "scenes/Dashboard/containers/Group-Content/GroupForcesView/execution";
import { GET_FORCES_EXECUTIONS } from "scenes/Dashboard/containers/Group-Content/GroupForcesView/queries";
import type {
  IExecution,
  IGroupExecutions,
} from "scenes/Dashboard/containers/Group-Content/GroupForcesView/types";
import { useDebouncedCallback, useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const GroupForcesView: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { groupName } = useParams<{ groupName: string }>();

  const [currentRow, setCurrentRow] = useState<IExecution>();
  const [isExecutionDetailsModalOpen, setIsExecutionDetailsModalOpen] =
    useState(false);
  const [filters, setFilters] = useState<IFilter<IExecution>[]>([
    {
      id: "status",
      key: "status",
      label: t("group.forces.status.title"),
      selectOptions: ["Secure", "Vulnerable"],
      type: "select",
    },
    {
      id: "strictness",
      key: "strictness",
      label: t("group.forces.strictness.title"),
      selectOptions: ["Strict", "Tolerant"],
      type: "select",
    },
    {
      id: "kind",
      key: "kind",
      label: t("group.forces.kind.title"),
      selectOptions: ["ALL", "DAST", "SAST"],
      type: "select",
    },
    {
      id: "gitRepo",
      key: "gitRepo",
      label: t("group.forces.gitRepo"),
      type: "text",
    },
    {
      id: "date",
      key: "date",
      label: t("group.forces.date"),
      type: "dateRange",
    },
  ]);
  const [sorting, setSorting] = useStoredState<SortingState>(
    "tblForcesExecutionsSorting",
    []
  );

  const headersExecutionTable: ColumnDef<IExecution>[] = useMemo(
    (): ColumnDef<IExecution>[] => [
      {
        accessorKey: "date",
        filterFn: filterDate,
        header: t("group.forces.date"),
      },
      {
        accessorKey: "status",
        cell: (cell: ICellHelper<IExecution>): JSX.Element =>
          statusFormatter(cell.getValue()),
        header: t("group.forces.status.title"),
      },
      {
        accessorFn: (row: IExecution): number => {
          return row.foundVulnerabilities.total;
        },
        header: String(t("group.forces.status.vulnerabilities")),
      },
      {
        accessorKey: "strictness",
        header: t("group.forces.strictness.title"),
      },
      {
        accessorKey: "kind",
        header: t("group.forces.kind.title"),
      },
      {
        accessorFn: (row: IExecution): string => {
          if (row.gitRepo === "unable to retrieve") {
            return "all roots";
          }

          return row.gitRepo;
        },
        header: t("group.forces.gitRepo"),
        id: "gitRepo",
      },
      {
        accessorKey: "executionId",
        header: t("group.forces.identifier"),
      },
    ],
    [t]
  );

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

  const { data, fetchMore, refetch } = useQuery<IGroupExecutions>(
    GET_FORCES_EXECUTIONS,
    {
      fetchPolicy: "cache-first",
      onError: handleQryErrors,
      variables: { first: 150, groupName, search: "" },
    }
  );
  const size = data?.group.executionsConnections.total;

  const executions: IExecution[] =
    data === undefined
      ? []
      : formatExecutions(data.group.executionsConnections.edges);

  const handleNextPage = useCallback(async (): Promise<void> => {
    const pageInfo =
      data === undefined
        ? { endCursor: "", hasNextPage: false }
        : data.group.executionsConnections.pageInfo;

    if (pageInfo.hasNextPage) {
      await fetchMore({ variables: { after: pageInfo.endCursor } });
    }
  }, [data, fetchMore]);

  const handleSearch = useDebouncedCallback((search: string): void => {
    void refetch({ search });
  }, 500);

  const filteredData = useFilters(executions, filters);

  return (
    <React.StrictMode>
      <p>{t("group.forces.tableAdvice")}</p>
      <Table
        columns={headersExecutionTable}
        data={filteredData}
        exportCsv={true}
        filters={<Filters filters={filters} setFilters={setFilters} />}
        id={"tblForcesExecutions"}
        onNextPage={handleNextPage}
        onRowClick={openSeeExecutionDetailsModal}
        onSearch={handleSearch}
        size={size}
        sortingSetter={setSorting}
        sortingState={sorting}
      />
      <Modal
        onClose={closeSeeExecutionDetailsModal}
        open={isExecutionDetailsModalOpen}
        title={t("group.forces.executionDetailsModal.title")}
      >
        {_.isNil(currentRow) ? undefined : <Execution {...currentRow} />}
      </Modal>
    </React.StrictMode>
  );
};

export { GroupForcesView };
