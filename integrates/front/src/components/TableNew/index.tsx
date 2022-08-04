import { faAngleDown, faAngleUp } from "@fortawesome/free-solid-svg-icons";
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
import type { ChangeEvent, ReactElement } from "react";
import React, { useState } from "react";
import { CSVLink } from "react-csv";
import { useTranslation } from "react-i18next";

import { ToggleFunction } from "./columnToggle";
import { PagMenu } from "./paginationMenu";
import { TableContainer } from "./styles";
import type { ITableProps } from "./types";

import {
  ButtonToolbarRow,
  SearchText,
  TableOptionsColBar,
} from "styles/styledComponents";

export const Tables = <TData extends object>(
  props: Readonly<ITableProps<TData>>
): JSX.Element => {
  const {
    id,
    data,
    columns,
    columnToggle = false,
    expandedRow = undefined,
    exportCsv = false,
    extraButtons = undefined,
    csvName = "Report",
    onRowClick = undefined,
    showPagination = data.length >= 8,
  } = props;
  const [columnVisibility, setColumnVisibility] = useState({});
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState("");
  const [expanded, setExpanded] = useState({});
  const { t } = useTranslation();

  function globalFilterHandler(event: ChangeEvent<HTMLInputElement>): void {
    setGlobalFilter(event.target.value);
  }

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
    onSortingChange: setSorting,
    state: {
      columnVisibility,
      expanded,
      globalFilter,
      sorting,
    },
  });

  return (
    <div className={"w-100"} id={id}>
      <TableOptionsColBar>
        {extraButtons !== undefined && extraButtons}
        <ButtonToolbarRow>
          <SearchText
            onChange={globalFilterHandler}
            placeholder={t("table.search")}
            value={globalFilter}
          />
        </ButtonToolbarRow>
      </TableOptionsColBar>
      {exportCsv && (
        <CSVLink data={data} filename={csvName}>
          {t("group.findings.exportCsv.text")}
        </CSVLink>
      )}
      {columnToggle && <ToggleFunction id={`${id}-togg`} table={table} />}
      <TableContainer
        isRowFunctional={onRowClick !== undefined}
        rowSize={"bold"}
      >
        <table>
          <thead>
            {table.getHeaderGroups().map(
              (headerGroup): ReactElement => (
                <tr key={headerGroup.id}>
                  {expandedRow !== undefined &&
                    (table.getIsAllRowsExpanded() ? (
                      <th>
                        <div
                          onClick={table.getToggleAllRowsExpandedHandler()}
                          onKeyPress={table.getToggleAllRowsExpandedHandler()}
                          role={"button"}
                          tabIndex={0}
                        >
                          <FontAwesomeIcon icon={faAngleUp} />
                        </div>
                      </th>
                    ) : (
                      <th>
                        <div
                          onClick={table.getToggleAllRowsExpandedHandler()}
                          onKeyPress={table.getToggleAllRowsExpandedHandler()}
                          role={"button"}
                          tabIndex={0}
                        >
                          <FontAwesomeIcon icon={faAngleDown} />
                        </div>
                      </th>
                    ))}
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
                            {{
                              asc: " 🔼",
                              desc: " 🔽",
                            }[header.column.getIsSorted() as string] ?? null}
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
                  <tr onClick={onRowClick?.(row)}>
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
      {showPagination && <PagMenu table={table} />}
    </div>
  );
};
