import {
  faAngleDown,
  faAngleUp,
  faSort,
  faSortDown,
  faSortUp,
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
import type { ChangeEvent, ChangeEventHandler, ReactElement } from "react";
import React, { useEffect, useState } from "react";
import { CSVLink } from "react-csv";
import { useTranslation } from "react-i18next";

import { ToggleFunction } from "./columnToggle";
import { Pagination } from "./Pagination";
import { TableContainer } from "./styles";
import type { ITableProps } from "./types";

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
  rowSelectionSetter = undefined,
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
  }

  const radioSelectionhandler =
    (row: Row<TData>): ChangeEventHandler =>
    (event: ChangeEvent<HTMLInputElement>): void => {
      setRowSelection({});
      row.toggleSelected();
      event.preventDefault();
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
                {t("group.findings.exportCsv.text")}
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
          <thead>
            {table.getHeaderGroups().map(
              (headerGroup): ReactElement => (
                <tr key={headerGroup.id}>
                  {expandedRow === undefined ? undefined : (
                    <th>
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
                    </th>
                  )}
                  {rowSelectionSetter !== undefined && (
                    <th>
                      {selectionMode === "checkbox" && (
                        <input
                          checked={table.getIsAllRowsSelected()}
                          onChange={table.getToggleAllRowsSelectedHandler()}
                          type={"checkbox"}
                        />
                      )}
                    </th>
                  )}
                  {headerGroup.headers.map(
                    (header): ReactElement => (
                      <th key={header.id}>
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
                                }[header.column.getIsSorted() as string] ??
                                faSort
                              }
                            />
                          </div>
                        )}
                      </th>
                    )
                  )}
                </tr>
              )
            )}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row): ReactElement => {
              return (
                <React.Fragment key={row.id}>
                  <tr>
                    {expandedRow !== undefined &&
                      (row.getIsExpanded() ? (
                        <td>
                          <div
                            onClick={row.getToggleExpandedHandler()}
                            onKeyPress={row.getToggleExpandedHandler()}
                            role={"button"}
                            tabIndex={0}
                          >
                            <FontAwesomeIcon icon={faAngleUp} />
                          </div>
                        </td>
                      ) : (
                        <td>
                          <div
                            onClick={row.getToggleExpandedHandler()}
                            onKeyPress={row.getToggleExpandedHandler()}
                            role={"button"}
                            tabIndex={0}
                          >
                            <FontAwesomeIcon icon={faAngleDown} />
                          </div>
                        </td>
                      ))}
                    {rowSelectionSetter !== undefined &&
                      (selectionMode === "radio" ? (
                        <td>
                          <input
                            checked={row.getIsSelected()}
                            name={"tableselection"}
                            onChange={radioSelectionhandler(row)}
                            type={selectionMode}
                          />
                        </td>
                      ) : (
                        <td>
                          <input
                            checked={row.getIsSelected()}
                            onChange={row.getToggleSelectedHandler()}
                            type={selectionMode}
                          />
                        </td>
                      ))}
                    {row.getVisibleCells().map(
                      (cell): ReactElement => (
                        <td key={cell.id}>
                          <div
                            onClick={onRowClick?.(row)}
                            onKeyPress={onRowClick?.(row)}
                            role={"button"}
                            tabIndex={0}
                          >
                            {flexRender(
                              cell.column.columnDef.cell,
                              cell.getContext()
                            )}
                          </div>
                        </td>
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
        <Pagination
          getPageCount={table.getPageCount}
          getState={table.getState}
          setPageIndex={table.setPageIndex}
          setPageSize={table.setPageSize}
          size={data.length}
        />
      ) : undefined}
    </div>
  );
};

export { Table };
