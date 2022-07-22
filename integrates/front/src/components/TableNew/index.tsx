import {
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  useReactTable,
} from "@tanstack/react-table";
import type { ColumnDef } from "@tanstack/react-table";
import type { ChangeEvent, ReactElement } from "react";
import React, { useState } from "react";

import { ToggleFunction } from "./columnToggle";

export interface ITableProps<TData> {
  id: string;
  data: TData[];
  columns: ColumnDef<TData>[];
  columnToggle?: boolean;
}

export const Tables = <TData extends Record<string, unknown>>(
  props: Readonly<ITableProps<TData>>
): JSX.Element => {
  const { id, data, columns, columnToggle = false } = props;
  const [columnVisibility, setColumnVisibility] = useState({});

  const table = useReactTable<TData>({
    columns,
    data,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    state: {
      columnVisibility,
    },
  });

  function firstPage(): void {
    table.setPageIndex(0);
  }
  function prevPage(): void {
    table.previousPage();
  }
  function nextPage(): void {
    table.nextPage();
  }
  function lastPage(): void {
    table.setPageIndex(table.getPageCount() - 1);
  }
  function pageIndex(event: ChangeEvent<HTMLInputElement>): void {
    const page = event.target.value ? Number(event.target.value) - 1 : 0;
    table.setPageIndex(page);
  }
  function pageRecords(event: ChangeEvent<HTMLSelectElement>): void {
    table.setPageSize(Number(event.target.value));
  }

  return (
    <div className={"w-100"} id={id}>
      {columnToggle && <ToggleFunction id={`${id}-togg`} table={table} />}
      <table>
        <thead>
          {table.getHeaderGroups().map(
            (headerGroup): ReactElement => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map(
                  (header): ReactElement => (
                    <th key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
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
              <tr key={row.id}>
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
      <div>
        <button disabled={!table.getCanPreviousPage()} onClick={firstPage}>
          {"<<"}
        </button>
        <button disabled={!table.getCanPreviousPage()} onClick={prevPage}>
          {"<"}
        </button>
        <button disabled={!table.getCanNextPage()} onClick={nextPage}>
          {">"}
        </button>
        <button disabled={!table.getCanPreviousPage()} onClick={lastPage}>
          {">>"}
        </button>
        <span>
          <strong>
            {`${
              table.getState().pagination.pageIndex + 1
            } of ${table.getPageCount()}`}
          </strong>
        </span>
        <span>
          {"Page: "}
          <input
            defaultValue={table.getState().pagination.pageIndex + 1}
            onChange={pageIndex}
            type={"number"}
          />
        </span>
        <select
          onChange={pageRecords}
          value={table.getState().pagination.pageSize}
        >
          {[10, 20].map(
            (pageSize): ReactElement => (
              <option key={pageSize} value={pageSize}>
                {`Show ${pageSize}`}
              </option>
            )
          )}
        </select>
      </div>
      {`${table.getRowModel().rows.length} Rows`}
    </div>
  );
};
