import { useQuery } from "@apollo/client";
import type { ColumnDef, Row } from "@tanstack/react-table";
import _ from "lodash";
import React, { useCallback } from "react";
import { useHistory } from "react-router-dom";

import { Table } from "components/Table";
import { GET_TODO_REATTACKS } from "scenes/Dashboard/containers/Tasks-Content/Reattacks/queries";
import type {
  IFindingFormatted,
  IGetTodoReattacks,
} from "scenes/Dashboard/containers/Tasks-Content/Reattacks/types";
import { formatFindings } from "scenes/Dashboard/containers/Tasks-Content/Reattacks/utils";
import { Logger } from "utils/logger";

export const TasksReattacks: React.FC = (): JSX.Element => {
  const { push } = useHistory();

  const columns: ColumnDef<IFindingFormatted>[] = [
    {
      accessorKey: "groupName",
      header: "Group Name",
    },
    {
      accessorKey: "title",
      header: "Type",
    },
    {
      accessorFn: (row: IFindingFormatted): string =>
        row.verificationSummary.requested,
      header: "Requested Vulns",
    },
    {
      accessorKey: "oldestReattackRequestedDate",
      header: "Reattack Date",
    },
  ];

  const { data } = useQuery<IGetTodoReattacks>(GET_TODO_REATTACKS, {
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.warning(
          "An error occurred fetching user findings from dashboard",
          error
        );
      });
    },
  });

  const dataset: IFindingFormatted[] = formatFindings(
    _.isUndefined(data) || _.isEmpty(data)
      ? []
      : _.flatten(data.me.findingReattacksConnection.edges)
  );

  const goToFinding = useCallback(
    (rowInfo: Row<IFindingFormatted>): ((event: React.FormEvent) => void) => {
      return (event: React.FormEvent): void => {
        push(
          `/groups/${rowInfo.original.groupName}/vulns/${rowInfo.original.id}/locations`
        );
        event.preventDefault();
      };
    },
    [push]
  );

  return (
    <React.StrictMode>
      <Table
        columns={columns}
        data={dataset}
        exportCsv={true}
        id={"tblTodoReattacks"}
        onRowClick={goToFinding}
      />
    </React.StrictMode>
  );
};
