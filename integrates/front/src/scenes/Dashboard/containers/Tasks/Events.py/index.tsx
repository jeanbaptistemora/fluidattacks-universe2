/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import type { ColumnDef } from "@tanstack/react-table";
import React from "react";

import { GET_TODO_EVENTS } from "./queries";
import type { IEventAttr, ITodoEvents } from "./types";

import { Table } from "components/TableNew";
import { filterDate } from "components/TableNew/filters/filterFunctions/filterDate";
import type { ICellHelper } from "components/TableNew/types";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { useDebouncedCallback } from "utils/hooks";

const tableColumns: ColumnDef<IEventAttr>[] = [
  {
    accessorFn: (row): string => `${row.groupName}`,
    enableColumnFilter: false,
    header: "Group Name",
  },
  {
    accessorFn: (row): string | undefined => row.root?.nickname,
    enableColumnFilter: false,
    header: "Root",
  },
  {
    accessorKey: "eventDate",
    filterFn: filterDate,
    header: "Event Date",
    meta: { filterType: "dateRange" },
  },
  {
    accessorKey: "detail",
    header: "Description",
  },
  {
    accessorKey: "eventType",
    header: "Type",
    meta: { filterType: "select" },
  },
  {
    accessorKey: "eventStatus",
    cell: (cell: ICellHelper<IEventAttr>): JSX.Element =>
      statusFormatter(cell.getValue()),
    header: "Status",
    meta: { filterType: "select" },
  },
];

const EventsTaskView: React.FC = (): JSX.Element => {
  const { data, refetch } = useQuery<ITodoEvents>(GET_TODO_EVENTS, {
    fetchPolicy: "cache-first",
    variables: { search: "" },
  });

  const Events =
    data === undefined
      ? []
      : data.me.pendingEvents.map((event): IEventAttr => event);

  const handleSearch = useDebouncedCallback((search: string): void => {
    void refetch({ search });
  }, 500);

  return (
    <div>
      <Table
        columnToggle={true}
        columns={tableColumns}
        data={Events}
        enableColumnFilters={true}
        exportCsv={false}
        id={"tblGroupVulnerabilities"}
        onSearch={handleSearch}
      />
    </div>
  );
};

export { EventsTaskView };
