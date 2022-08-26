import {
  faAngleDown,
  faAngleUp,
  faSort,
  faSortDown,
  faSortUp,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { RowData, Table } from "@tanstack/react-table";
import { flexRender } from "@tanstack/react-table";
import React from "react";

import type { ITableProps } from "./types";

import { Gap } from "components/Layout";

interface IHeadProps<TData extends RowData>
  extends Pick<
    ITableProps<TData>,
    "expandedRow" | "rowSelectionSetter" | "selectionMode"
  > {
  table: Table<TData>;
}

const Head = <TData extends RowData>({
  expandedRow,
  rowSelectionSetter,
  selectionMode,
  table,
}: IHeadProps<TData>): JSX.Element => {
  return (
    <thead>
      {table.getHeaderGroups().map((headerGroup): JSX.Element => {
        return (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map((header): JSX.Element => {
              return (
                <React.Fragment key={header.id}>
                  <th>
                    <Gap>
                      {header === headerGroup.headers[0] &&
                        expandedRow !== undefined && (
                          <div
                            onClick={table.getToggleAllRowsExpandedHandler()}
                            onKeyPress={table.getToggleAllRowsExpandedHandler()}
                            role={"button"}
                            tabIndex={0}
                          >
                            <FontAwesomeIcon
                              icon={
                                table.getIsAllRowsExpanded()
                                  ? faAngleUp
                                  : faAngleDown
                              }
                            />
                          </div>
                        )}
                      {header === headerGroup.headers[0] &&
                        rowSelectionSetter !== undefined &&
                        selectionMode === "checkbox" && (
                          <input
                            checked={table.getIsAllRowsSelected()}
                            onClick={table.getToggleAllRowsSelectedHandler()}
                            type={"checkbox"}
                          />
                        )}
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
                          &nbsp;
                          <FontAwesomeIcon
                            icon={
                              {
                                asc: faSortUp,
                                desc: faSortDown,
                              }[header.column.getIsSorted() as string] ?? faSort
                            }
                          />
                        </div>
                      )}
                    </Gap>
                  </th>
                </React.Fragment>
              );
            })}
          </tr>
        );
      })}
    </thead>
  );
};

export { Head };
