/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { faDownload } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  getCoreRowModel,
  getFacetedMinMaxValues,
  getFacetedRowModel,
  getFacetedUniqueValues,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";
import type {
  ColumnFiltersState,
  FilterFn,
  PaginationState,
  Row,
  RowData,
  SortingState,
} from "@tanstack/react-table";
import _ from "lodash";
import type { ChangeEvent, MouseEvent, MouseEventHandler } from "react";
import React, { isValidElement, useCallback, useEffect, useState } from "react";
import { CSVLink } from "react-csv";
import { useTranslation } from "react-i18next";

import { Body } from "./Body";
import { ToggleFunction } from "./columnToggle";
import { Filters } from "./filters";
import { Head } from "./Head";
import { Pagination } from "./Pagination";
import { TableContainer } from "./styles";
import type { ITableProps } from "./types";

import { Button } from "components/Button";
import { Gap } from "components/Layout/Gap";
import { SearchText } from "styles/styledComponents";

const Table = <TData extends RowData>({
  columns,
  columnFilterSetter = undefined,
  columnFilterState = undefined,
  columnToggle = false,
  columnVisibilityState = undefined,
  columnVisibilitySetter = undefined,
  csvName = "Report",
  data,
  enableColumnFilters = false,
  enableRowSelection = true,
  enableSearchBar = true,
  expandedRow = undefined,
  exportCsv = false,
  extraButtons = undefined,
  id,
  initState = undefined,
  onNextPage = undefined,
  onRowClick = undefined,
  onSearch = undefined,
  paginationSetter = undefined,
  paginationState = undefined,
  rowSelectionSetter = undefined,
  rowSelectionState = undefined,
  selectionMode = "checkbox",
  sortingSetter = undefined,
  sortingState = undefined,
}: Readonly<ITableProps<TData>>): JSX.Element => {
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [pagination, setPagination] = useState<PaginationState>({
    pageIndex: 0,
    pageSize: 10,
  });
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

  const radioSelectionhandler = useCallback(
    (row: Row<TData>): MouseEventHandler =>
      (event: MouseEvent<HTMLInputElement>): void => {
        event.stopPropagation();
        setRowSelection({});
        row.toggleSelected();
      },
    []
  );

  const filterFun: FilterFn<TData> = (
    row: Row<TData>,
    columnId: string,
    filterValue: string
  ): boolean => {
    return String(row.getValue(columnId))
      .toLowerCase()
      .includes(filterValue.toLowerCase());
  };

  const table = useReactTable<TData>({
    columns,
    data,
    enableColumnFilters,
    enableRowSelection,
    getCoreRowModel: getCoreRowModel(),
    getFacetedMinMaxValues: getFacetedMinMaxValues(),
    getFacetedRowModel: getFacetedRowModel(),
    getFacetedUniqueValues: getFacetedUniqueValues(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getRowCanExpand: (): boolean => expandedRow !== undefined,
    getSortedRowModel: getSortedRowModel(),
    globalFilterFn: filterFun,
    onColumnFiltersChange: columnFilterSetter
      ? columnFilterSetter
      : setColumnFilters,
    onColumnVisibilityChange: columnVisibilitySetter
      ? columnVisibilitySetter
      : setColumnVisibility,
    onExpandedChange: setExpanded,
    onGlobalFilterChange: setGlobalFilter,
    onPaginationChange: paginationSetter ? paginationSetter : setPagination,
    onRowSelectionChange: setRowSelection,
    onSortingChange: sortingSetter ? sortingSetter : setSorting,
    state: {
      columnFilters: columnFilterState ? columnFilterState : columnFilters,
      columnVisibility: columnVisibilityState
        ? columnVisibilityState
        : columnVisibility,
      expanded,
      globalFilter,
      pagination: paginationState ? paginationState : pagination,
      rowSelection,
      sorting: sortingState ? sortingState : sorting,
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
        <div className={"flex justify-between"}>
          {enableSearchBar ? (
            <SearchText
              onChange={globalFilterHandler}
              placeholder={t("table.search")}
              value={globalFilter}
            />
          ) : undefined}
          {enableColumnFilters ? <Filters table={table} /> : undefined}
        </div>
      </div>
      <TableContainer clickable={onRowClick !== undefined}>
        <table>
          <Head
            expandedRow={expandedRow}
            rowSelectionSetter={rowSelectionSetter}
            selectionMode={selectionMode}
            table={table}
          />
          <Body
            data={data}
            expandedRow={expandedRow}
            onRowClick={onRowClick}
            radioSelectionhandler={radioSelectionhandler}
            rowSelectionSetter={rowSelectionSetter}
            selectionMode={selectionMode}
            table={table}
          />
        </table>
      </TableContainer>
      {data.length > 10 ? (
        <Pagination onNextPage={onNextPage} size={data.length} table={table} />
      ) : undefined}
    </div>
  );
};

export { Table };
