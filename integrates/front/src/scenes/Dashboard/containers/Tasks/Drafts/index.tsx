/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import type { ColumnDef, Row } from "@tanstack/react-table";
import _ from "lodash";
import React from "react";
import { useHistory } from "react-router-dom";

import { Table } from "components/Table";
import { filterDate } from "components/Table/filters/filterFunctions/filterDate";
import type { ICellHelper } from "components/Table/types";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { GET_TODO_DRAFTS } from "scenes/Dashboard/containers/Tasks/Drafts/queries";
import type {
  IGetTodoDrafts,
  ITodoDraftAttr,
} from "scenes/Dashboard/containers/Tasks/Drafts/types";
import { Logger } from "utils/logger";

export const TasksDrafts: React.FC = (): JSX.Element => {
  const { push } = useHistory();

  const hackerFormatter = (value: string): JSX.Element => {
    return <div className={`tl truncate`}>{value}</div>;
  };

  const columns: ColumnDef<ITodoDraftAttr>[] = [
    {
      accessorKey: "reportDate",
      filterFn: filterDate,
      header: "Date",
      meta: { filterType: "dateRange" },
    },

    {
      accessorKey: "title",
      header: "Type",
    },
    {
      accessorKey: "severityScore",
      header: "Severity",
      meta: { filterType: "number" },
    },
    {
      accessorKey: "openVulnerabilities",
      header: "Open Vulns.",
      meta: { filterType: "number" },
    },
    {
      accessorKey: "groupName",
      header: "Group Name",
    },
    {
      accessorKey: "hacker",
      cell: (cell: ICellHelper<ITodoDraftAttr>): JSX.Element =>
        hackerFormatter(cell.getValue()),
      header: "Hacker",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "currentState",
      cell: (cell: ICellHelper<ITodoDraftAttr>): JSX.Element =>
        statusFormatter(cell.getValue()),
      header: "State",
      meta: { filterType: "select" },
    },
  ];

  const { data } = useQuery<IGetTodoDrafts>(GET_TODO_DRAFTS, {
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.warning(
          "An error occurred fetching user drafts from dashboard",
          error
        );
      });
    },
  });

  const dataset: ITodoDraftAttr[] =
    _.isUndefined(data) || _.isEmpty(data) ? [] : _.flatten(data.me.drafts);

  function goToDraft(
    rowInfo: Row<ITodoDraftAttr>
  ): (event: React.FormEvent) => void {
    return (event: React.FormEvent): void => {
      push(
        `/groups/${rowInfo.original.groupName}/drafts/${rowInfo.original.id}/locations`
      );
      event.preventDefault();
    };
  }

  return (
    <React.StrictMode>
      <Table
        columns={columns}
        data={dataset}
        enableColumnFilters={true}
        exportCsv={true}
        id={"tblTodoDrafts"}
        onRowClick={goToDraft}
      />
    </React.StrictMode>
  );
};
