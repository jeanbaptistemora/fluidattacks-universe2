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
import React, { useEffect, useState } from "react";
import { CSVLink } from "react-csv";
import { useTranslation } from "react-i18next";

import { ToggleFunction } from "./columnToggle";
import { PagMenu } from "./paginationMenu";
import { TableContainer } from "./styles";
import type { ITableProps, ITablepropsWithRowSel } from "./types";

import { Gap } from "components/Layout/Gap";
import { SearchText } from "styles/styledComponents";

export const Tables = <TData extends object>(
  props: Readonly<ITableProps<TData>> | Readonly<ITablepropsWithRowSel<TData>>
): JSX.Element => {
  const {
    id,
    data,
    columns,
    initialState = undefined,
    columnToggle = false,
    expandedRow = undefined,
    exportCsv = false,
    extraButtons = undefined,
    csvName = "Report",
    enableSearchBar = true,
    onRowClick = undefined,
    rowSelectionSetter = undefined,
    showPagination = data.length >= 8,
  } = props;

  const [columnVisibility, setColumnVisibility] = useState(
    initialState?.columnVisibility ?? {}
  );
  const [sorting, setSorting] = useState<SortingState>(
    initialState?.sorting ?? []
  );
  const [globalFilter, setGlobalFilter] = useState(
    initialState?.globalFilter ?? ""
  );
  const [expanded, setExpanded] = useState(initialState?.expanded ?? {});
  const [rowSelection, setRowSelection] = useState(
    initialState?.rowSelection ?? {}
  );
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
    <div className={"w-100"} id={id}>
      <div className={"flex w-100"}>
        <div className={`flex flex-wrap pa0 w-100`}>
          <Gap>
            {extraButtons !== undefined && extraButtons}
            {columnToggle && <ToggleFunction id={`${id}-togg`} table={table} />}
            {exportCsv && (
              <CSVLink data={data} filename={csvName}>
                {t("group.findings.exportCsv.text")}
              </CSVLink>
            )}
          </Gap>
        </div>
        {enableSearchBar && (
          <div className={"d-flex justify-content-end w-25"}>
            <SearchText
              onChange={globalFilterHandler}
              placeholder={t("table.search")}
              value={globalFilter}
            />
          </div>
        )}
      </div>
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
                  {rowSelectionSetter !== undefined && (
                    <th>
                      <input
                        checked={table.getIsAllRowsSelected()}
                        onChange={table.getToggleAllRowsSelectedHandler()}
                        type={"checkbox"}
                      />
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
                    {rowSelectionSetter !== undefined && (
                      <td>
                        <input
                          checked={row.getIsSelected()}
                          onChange={row.getToggleSelectedHandler()}
                          type={"checkbox"}
                        />
                      </td>
                    )}
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
      {showPagination && <PagMenu table={table} />}
    </div>
  );
};
