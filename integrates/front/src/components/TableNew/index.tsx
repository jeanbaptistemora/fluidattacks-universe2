import {
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";
import type { ColumnDef, SortingState } from "@tanstack/react-table";
import type { ReactElement } from "react";
import React, { useState } from "react";
import { CSVLink } from "react-csv";

import { ToggleFunction } from "./columnToggle";
import { PagMenu } from "./paginationMenu";

export interface ITableProps<TData> {
  id: string;
  data: TData[];
  columns: ColumnDef<TData>[];
  columnToggle?: boolean;
  exportCsv?: boolean;
  csvName?: string;
  rowFunction?: () => void;
}

export const Tables = <TData extends Record<string, unknown>>(
  props: Readonly<ITableProps<TData>>
): JSX.Element => {
  const {
    id,
    data,
    columns,
    columnToggle = false,
    exportCsv = false,
    csvName = "Report",
    rowFunction = undefined,
  } = props;
  const [columnVisibility, setColumnVisibility] = useState({});
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState("");

  const table = useReactTable<TData>({
    columns,
    data,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onGlobalFilterChange: setGlobalFilter,
    onSortingChange: setSorting,
    state: {
      columnVisibility,
      globalFilter,
      sorting,
    },
  });

  return (
    <div className={"w-100"} id={id}>
      {exportCsv && (
        <CSVLink data={data} filename={csvName}>
          {"Reporte"}
        </CSVLink>
      )}
      {columnToggle && <ToggleFunction id={`${id}-togg`} table={table} />}
      <table>
        <thead>
          {table.getHeaderGroups().map(
            (headerGroup): ReactElement => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map(
                  (header): ReactElement => (
                    <th key={header.id}>
                      {header.isPlaceholder ? null : (
                        <div
                          className={
                            header.column.getCanSort()
                              ? "cursor-pointer select-none"
                              : ""
                          }
                          onClick={header.column.getToggleSortingHandler()}
                          onKeyPress={header.column.getToggleSortingHandler()}
                          role={"button"}
                          tabIndex={0}
                        >
                          {flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                          {{
                            asc: " 🔼",
                            desc: " 🔽",
                          }[header.column.getIsSorted() as string] ?? null}
                        </div>
                      )}
                    </th>
                  )
                )}
              </tr>
            )
          )}
        </thead>
        <tbody>
          {table.getRowModel().rows.map(
            (row): ReactElement => (
              <tr key={row.id} onClick={rowFunction}>
                {row.getVisibleCells().map(
                  (cell): ReactElement => (
                    <td key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </td>
                  )
                )}
              </tr>
            )
          )}
        </tbody>
      </table>
      <PagMenu table={table} />
    </div>
  );
};
