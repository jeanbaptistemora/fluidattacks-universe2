/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
import type { FormEvent } from "react";

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
  function allRowExpansionHandler(): (event: FormEvent) => void {
    return (event: FormEvent): void => {
      event.stopPropagation();
      table.toggleAllRowsExpanded();
    };
  }

  function allRowSelectionHandler(): (event: FormEvent) => void {
    return (event: FormEvent): void => {
      event.stopPropagation();
      if (table.getIsSomeRowsSelected() || table.getIsAllRowsSelected()) {
        table.resetRowSelection();
      } else {
        table.toggleAllRowsSelected();
      }
    };
  }

  return (
    <thead>
      {table.getHeaderGroups().map((headerGroup): JSX.Element => {
        return (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map((header): JSX.Element => {
              return (
                <React.Fragment key={header.id}>
                  <th
                    className={
                      header.column.getCanSort()
                        ? "cursor-pointer select-none"
                        : ""
                    }
                    onClick={header.column.getToggleSortingHandler()}
                  >
                    <Gap>
                      {header === headerGroup.headers[0] &&
                        expandedRow !== undefined && (
                          <div
                            onClick={allRowExpansionHandler()}
                            onKeyPress={allRowExpansionHandler()}
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
                            checked={
                              table.getIsSomeRowsSelected() ||
                              table.getIsAllRowsSelected()
                            }
                            onClick={allRowSelectionHandler()}
                            type={"checkbox"}
                          />
                        )}
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