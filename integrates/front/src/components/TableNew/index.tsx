import {
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  useReactTable,
} from "@tanstack/react-table";
import type { ColumnDef } from "@tanstack/react-table";
import type { ReactElement } from "react";
import React, { useState } from "react";

import { ToggleFunction } from "./columnToggle";
import { PagMenu } from "./paginationMenu";

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
      <PagMenu table={table} />
    </div>
  );
};
