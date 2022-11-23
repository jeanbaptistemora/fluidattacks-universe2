import { useQuery } from "@apollo/client";
import type { ColumnDef, Row } from "@tanstack/react-table";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import type { FormEvent } from "react";
import React from "react";
import { useHistory } from "react-router-dom";

import { GET_TODO_EVENTS } from "./queries";
import type { IEventAttr, ITodoEvents } from "./types";
import { formatTodoEvents } from "./utils";

import { Table } from "components/Table";
import { filterDate } from "components/Table/filters/filterFunctions/filterDate";
import type { ICellHelper } from "components/Table/types";
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
  const { push } = useHistory();
  const { data, refetch } = useQuery<ITodoEvents>(GET_TODO_EVENTS, {
    fetchPolicy: "cache-first",
    variables: { search: "" },
  });

  const allEvents = data === undefined ? [] : data.me.pendingEvents;
  const Events = formatTodoEvents(allEvents);

  const handleSearch = useDebouncedCallback((search: string): void => {
    void refetch({ search });
  }, 500);

  function goToEvent(rowInfo: Row<IEventAttr>): (event: FormEvent) => void {
    return (event: FormEvent): void => {
      mixpanel.track("ReadEvent");
      push(
        `/groups/${rowInfo.original.groupName}/events/${rowInfo.original.id}/description`
      );
      event.preventDefault();
    };
  }

  return (
    <div>
      <Table
        columns={tableColumns}
        data={Events}
        enableColumnFilters={true}
        exportCsv={true}
        id={"tblGroupVulnerabilities"}
        onRowClick={goToEvent}
        onSearch={handleSearch}
      />
    </div>
  );
};

export { EventsTaskView };
