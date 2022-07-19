import {
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import type { ColumnDef } from "@tanstack/react-table";
import type { ReactElement } from "react";
import React from "react";

export interface ITableProps<TData> {
  id: string;
  data: TData[];
  columns: ColumnDef<TData>[];
}

export const Tables = <TData extends Record<string, unknown>>(
  props: ITableProps<TData>
): JSX.Element => {
  const { id, data, columns } = props;

  const table = useReactTable<TData>({
    columns,
    data,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className={"w-100"} id={id}>
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
