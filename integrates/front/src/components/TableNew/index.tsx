import {
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";
import type { SortingState } from "@tanstack/react-table";
import type { ReactElement } from "react";
import React, { useState } from "react";
import { CSVLink } from "react-csv";

import { ToggleFunction } from "./columnToggle";
import { PagMenu } from "./paginationMenu";
import { TableContainer } from "./styles";
import type { ITableProps } from "./types";

export const Tables = <TData extends object>(
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
    showPagination = data.length >= 8,
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
      <TableContainer
        isRowFunctional={rowFunction !== undefined}
        rowSize={"bold"}
      >
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
                <tr key={row.id} onClick={rowFunction?.(row)}>
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
      </TableContainer>
      {showPagination && <PagMenu table={table} />}
    </div>
  );
};
