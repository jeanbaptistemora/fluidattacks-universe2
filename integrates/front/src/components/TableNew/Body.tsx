import { faAngleDown, faAngleUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { Row, RowData, Table } from "@tanstack/react-table";
import { flexRender } from "@tanstack/react-table";
import _ from "lodash";
import type { ChangeEventHandler } from "react";
import React from "react";
import { useTranslation } from "react-i18next";

import type { ITableProps } from "./types";

import { Gap } from "components/Layout";

interface IBodyProps<TData extends RowData>
  extends Pick<
    ITableProps<TData>,
    | "data"
    | "expandedRow"
    | "onRowClick"
    | "rowSelectionSetter"
    | "selectionMode"
  > {
  radioSelectionhandler: (row: Row<TData>) => ChangeEventHandler;
  table: Table<TData>;
}

const Body = <TData extends RowData>({
  data,
  expandedRow,
  onRowClick,
  radioSelectionhandler,
  rowSelectionSetter,
  selectionMode,
  table,
}: IBodyProps<TData>): JSX.Element => {
  const { t } = useTranslation();

  return (
    <tbody>
      {_.isEmpty(data) && <tr>{t("table.noDataIndication")}</tr>}
      {table.getRowModel().rows.map((row): JSX.Element => {
        return (
          <React.Fragment key={row.id}>
            <tr>
              {row.getVisibleCells().map(
                (cell): JSX.Element => (
                  <React.Fragment key={cell.id}>
                    <td>
                      <Gap>
                        {expandedRow !== undefined &&
                          cell === row.getVisibleCells()[0] &&
                          (row.getIsExpanded() ? (
                            <div
                              onClick={row.getToggleExpandedHandler()}
                              onKeyPress={row.getToggleExpandedHandler()}
                              role={"button"}
                              tabIndex={0}
                            >
                              <FontAwesomeIcon icon={faAngleUp} />
                            </div>
                          ) : (
                            <div
                              onClick={row.getToggleExpandedHandler()}
                              onKeyPress={row.getToggleExpandedHandler()}
                              role={"button"}
                              tabIndex={0}
                            >
                              <FontAwesomeIcon icon={faAngleDown} />
                            </div>
                          ))}
                        <label>
                          <Gap>
                            {cell === row.getVisibleCells()[0] &&
                              rowSelectionSetter !== undefined &&
                              (selectionMode === "radio" ? (
                                <input
                                  checked={row.getIsSelected()}
                                  onChange={radioSelectionhandler(row)}
                                  type={selectionMode}
                                />
                              ) : (
                                <input
                                  checked={row.getIsSelected()}
                                  onChange={row.getToggleSelectedHandler()}
                                  type={selectionMode}
                                />
                              ))}
                            {onRowClick === undefined ? (
                              <div>
                                {flexRender(
                                  cell.column.columnDef.cell,
                                  cell.getContext()
                                )}
                              </div>
                            ) : (
                              <div
                                onClick={onRowClick(row)}
                                onKeyPress={onRowClick(row)}
                                role={"button"}
                                tabIndex={0}
                              >
                                {flexRender(
                                  cell.column.columnDef.cell,
                                  cell.getContext()
                                )}
                              </div>
                            )}
                          </Gap>
                        </label>
                      </Gap>
                    </td>
                  </React.Fragment>
                )
              )}
            </tr>
            {row.getIsExpanded() && (
              <tr>
                <td colSpan={row.getVisibleCells().length}>
                  {expandedRow?.(row)}
                </td>
              </tr>
            )}
          </React.Fragment>
        );
      })}
    </tbody>
  );
};

export { Body };
