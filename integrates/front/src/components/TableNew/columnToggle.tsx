import type { Table } from "@tanstack/react-table";
import type { ReactElement } from "react";
import React from "react";

export interface IToggleProps<TData> {
  id: string;
  table: Table<TData>;
}

export const ToggleFunction = <TData extends Record<string, unknown>>(
  props: IToggleProps<TData>
): JSX.Element => {
  const { id, table } = props;

  return (
    <div id={id}>
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
  );
};
