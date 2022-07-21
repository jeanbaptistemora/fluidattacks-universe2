import {
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import type { ColumnDef } from "@tanstack/react-table";
import type { ReactElement } from "react";
import React, { useState } from "react";

export interface ITableProps<TData> {
  id: string;
  data: TData[];
  columns: ColumnDef<TData>[];
}

export const Tables = <TData extends Record<string, unknown>>(
  props: ITableProps<TData>
): JSX.Element => {
  const { id, data, columns } = props;
  const [columnVisibility, setColumnVisibility] = useState({});

  const table = useReactTable<TData>({
    columns,
    data,
    getCoreRowModel: getCoreRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    state: {
      columnVisibility,
    },
  });

  return (
    <div className={"w-100"} id={id}>
      <div>
        <label>
          <input
            checked={table.getIsAllColumnsVisible()}
            onChange={table.getToggleAllColumnsVisibilityHandler()}
            type={"checkbox"}
          />{" "}
          {"Toggle All"}
        </label>
        {table.getAllLeafColumns().map((column): ReactElement => {
          return (
            <div key={column.id}>
              <label>
                <input
                  checked={column.getIsVisible()}
                  onChange={column.getToggleVisibilityHandler()}
                  type={"checkbox"}
                />{" "}
                {column.id}
              </label>
            </div>
          );
        })}
      </div>
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
    </div>
  );
};
