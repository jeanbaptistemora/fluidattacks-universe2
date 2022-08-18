import {
  faAngleDown,
  faAngleUp,
  faDownload,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { rankItem } from "@tanstack/match-sorter-utils";
import {
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";
import type {
  FilterFn,
  FilterMeta,
  Row,
  SortingState,
} from "@tanstack/react-table";
import _ from "lodash";
import type { ChangeEvent, ChangeEventHandler, ReactElement } from "react";
import React, { isValidElement, useEffect, useState } from "react";
import { CSVLink } from "react-csv";
import { useTranslation } from "react-i18next";

import { ToggleFunction } from "./columnToggle";
import { Head } from "./Head";
import { Pagination } from "./Pagination";
import { TableContainer } from "./styles";
import type { ITableProps } from "./types";

import { Button } from "components/Button";
import { Gap } from "components/Layout/Gap";
import { SearchText } from "styles/styledComponents";

const Table = <TData extends object>({
  columns,
  columnToggle = false,
  csvName = "Report",
  data,
  enableSearchBar = true,
  expandedRow = undefined,
  exportCsv = false,
  extraButtons = undefined,
  id,
  initState = undefined,
  onRowClick = undefined,
  onSearch = undefined,
  onNextPage = undefined,
  rowSelectionSetter = undefined,
  rowSelectionState = undefined,
  selectionMode = "checkbox",
}: Readonly<ITableProps<TData>>): JSX.Element => {
  const [columnVisibility, setColumnVisibility] = useState(
    initState?.columnVisibility ?? {}
  );
  const [sorting, setSorting] = useState<SortingState>(
    initState?.sorting ?? []
  );
  const [globalFilter, setGlobalFilter] = useState(
    initState?.globalFilter ?? ""
  );
  const [expanded, setExpanded] = useState(initState?.expanded ?? {});
  const [rowSelection, setRowSelection] = useState(
    initState?.rowSelection ?? {}
  );
  const { t } = useTranslation();

  function globalFilterHandler(event: ChangeEvent<HTMLInputElement>): void {
    setGlobalFilter(event.target.value);

    if (onSearch) {
      onSearch(event.target.value);
    }
  }

  const radioSelectionhandler =
    (row: Row<TData>): ChangeEventHandler =>
    (event: ChangeEvent<HTMLInputElement>): void => {
      event.stopPropagation();
      setRowSelection({});
      row.toggleSelected();
    };

  const filterFun: FilterFn<TData> = (
    row: Row<TData>,
    columnId: string,
    value: string,
    addMeta: (meta: FilterMeta) => void
  ): boolean => {
    const itemRank = rankItem(row.getValue(columnId), value);
    addMeta({ itemRank });

    return itemRank.passed;
  };

  const table = useReactTable<TData>({
    columns,
    data,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getRowCanExpand: (): boolean => expandedRow !== undefined,
    getSortedRowModel: getSortedRowModel(),
    globalFilterFn: filterFun,
    onColumnVisibilityChange: setColumnVisibility,
    onExpandedChange: setExpanded,
    onGlobalFilterChange: setGlobalFilter,
    onRowSelectionChange: setRowSelection,
    onSortingChange: setSorting,
    state: {
      columnVisibility,
      expanded,
      globalFilter,
      rowSelection,
      sorting,
    },
  });

  /*
   * Next useEffect() takes the information of rowSelectionState
   * (row originals) and selects the equivalent rows in the rowSelection so
   * both are in sync, this is to support unselecting rows outside table
   */

  useEffect((): void => {
    if (rowSelectionState === undefined) {
      return undefined;
    }
    table.getRowModel().rows.forEach((row: Row<TData>): void => {
      if (
        _.some(rowSelectionState, (selected): boolean =>
          _.isEqualWith(
            row.original,
            selected,
            (val1, val2): boolean | undefined => {
              if (
                (_.isFunction(val1) && _.isFunction(val2)) ||
                (_.isObject(val1) && isValidElement(val1))
              ) {
                return true;
              }

              return undefined;
            }
          )
        )
      ) {
        if (row.getIsSelected()) {
          return undefined;
        }
        row.toggleSelected();
      } else {
        if (row.getIsSelected()) {
          row.toggleSelected();
        }

        return undefined;
      }

      return undefined;
    });

    return undefined;
  }, [rowSelectionState, table]);

  useEffect((): void => {
    rowSelectionSetter?.(
      table
        .getSelectedRowModel()
        .flatRows.map((row: Row<TData>): TData => row.original)
    );
  }, [rowSelection, rowSelectionSetter, table]);

  return (
    <div className={"comp-table"} id={id}>
      <div className={"flex justify-between"}>
        <div>
          <Gap>
            {extraButtons}
            {columnToggle ? <ToggleFunction table={table} /> : undefined}
            {exportCsv ? (
              <CSVLink data={data as object[]} filename={csvName}>
                <Button variant={"ghost"}>
                  <FontAwesomeIcon icon={faDownload} />
                  &nbsp;
                  {t("group.findings.exportCsv.text")}
                </Button>
              </CSVLink>
            ) : undefined}
          </Gap>
        </div>
        {enableSearchBar ? (
          <div>
            <SearchText
              onChange={globalFilterHandler}
              placeholder={t("table.search")}
              value={globalFilter}
            />
          </div>
        ) : undefined}
      </div>
      <TableContainer clickable={onRowClick !== undefined}>
        <table>
          <Head
            expandedRow={expandedRow}
            rowSelectionSetter={rowSelectionSetter}
            selectionMode={selectionMode}
            table={table}
          />
          <tbody>
            {_.isEmpty(data) && <tr>{t("table.noDataIndication")}</tr>}
            {table.getRowModel().rows.map((row): ReactElement => {
              return (
                <React.Fragment key={row.id}>
                  <tr>
                    {row.getVisibleCells().map(
                      (cell): ReactElement => (
                        <React.Fragment key={cell.id}>
                          <td>
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
                            </label>
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
        </table>
      </TableContainer>
      {data.length > 10 ? (
        <Pagination onNextPage={onNextPage} size={data.length} table={table} />
      ) : undefined}
    </div>
  );
};

export { Table };
