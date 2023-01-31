import {
  faFileExport,
  faMagnifyingGlass,
} from "@fortawesome/free-solid-svg-icons";
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
  RowData,
  SortingState,
  Row as TableRow,
} from "@tanstack/react-table";
import _ from "lodash";
import type { ChangeEvent, ChangeEventHandler } from "react";
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
import { Container } from "components/Container";
import { FormikInput } from "components/Input/Formik";
import { Col, Row } from "components/Layout";
import { Text } from "components/Text";
import { flattenData } from "utils/formatHelpers";
import { useStoredState } from "utils/hooks";

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
  filters = undefined,
  id,
  onNextPage = undefined,
  onRowClick = undefined,
  onSearch = undefined,
  rowSelectionSetter = undefined,
  rowSelectionState = undefined,
  selectionMode = "checkbox",
  searchPlaceholder,
  size = undefined,
  sortingSetter = undefined,
  sortingState = undefined,
}: Readonly<ITableProps<TData>>): JSX.Element => {
  const [pagSize, setPagSize] = useStoredState("pagSize", 10);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [pagination, setPagination] = useState<PaginationState>({
    pageIndex: 0,
    pageSize: pagSize,
  });
  const [columnVisibility, setColumnVisibility] = useState({});
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState("");
  const [expanded, setExpanded] = useState({});
  const [rowSelection, setRowSelection] = useState({});
  const { t } = useTranslation();

  const globalFilterHandler = useCallback(
    (event: ChangeEvent<HTMLInputElement>): void => {
      setGlobalFilter(event.target.value);

      if (onSearch) {
        onSearch(event.target.value);
      }
    },
    [onSearch]
  );

  const radioSelectionhandler = useCallback(
    (row: TableRow<TData>): ChangeEventHandler =>
      (event: ChangeEvent<HTMLInputElement>): void => {
        event.stopPropagation();
        setRowSelection({});
        row.toggleSelected();
      },
    []
  );

  const filterFun: FilterFn<TData> = (
    row: TableRow<TData>,
    columnId: string,
    filterValue: string
  ): boolean => {
    return String(row.getValue(columnId))
      .toLowerCase()
      .includes(filterValue.toLowerCase());
  };

  const table = useReactTable<TData>({
    autoResetAll: false,
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
    onPaginationChange: setPagination,
    onRowSelectionChange: setRowSelection,
    onSortingChange: sortingSetter ? sortingSetter : setSorting,
    state: {
      columnFilters: columnFilterState ? columnFilterState : columnFilters,
      columnVisibility: columnVisibilityState
        ? columnVisibilityState
        : columnVisibility,
      expanded,
      globalFilter,
      pagination,
      rowSelection,
      sorting: sortingState ? sortingState : sorting,
    },
  });

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  function helper(val1: any, val2: any): boolean | undefined {
    if (
      (_.isFunction(val1) && _.isFunction(val2)) ||
      (_.isObject(val1) && isValidElement(val1))
    ) {
      return true;
    }

    return undefined;
  }

  /*
   * Next useEffect() takes the information of rowSelectionState
   * (row originals) and selects the equivalent rows in the rowSelection so
   * both are in sync, this is to support unselecting rows outside table
   */

  useEffect((): void => {
    if (rowSelectionState === undefined) {
      return undefined;
    }
    table.getRowModel().rows.forEach((row: TableRow<TData>): void => {
      if (
        _.some(rowSelectionState, (selected): boolean =>
          _.isEqualWith(row.original, selected, helper)
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
        .flatRows.map((row: TableRow<TData>): TData => row.original)
    );
  }, [rowSelection, rowSelectionSetter, table]);

  useEffect((): void => {
    setPagSize(pagination.pageSize);

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pagination]);

  return (
    <div className={"w-100"} id={id}>
      <Container scroll={"none"}>
        <Row justify={"end"}>
          <Col lg={20}>
            {enableSearchBar ? (
              <Container>
                <FormikInput
                  childLeft={
                    <Container pl={"5px"} scroll={"none"}>
                      <FontAwesomeIcon icon={faMagnifyingGlass} />
                    </Container>
                  }
                  field={{
                    name: "search",
                    onBlur: (): void => undefined,
                    onChange: globalFilterHandler,
                    value: globalFilter,
                  }}
                  form={{ errors: {}, touched: {} }}
                  name={"search"}
                  placeholder={
                    searchPlaceholder === undefined
                      ? t("table.search")
                      : searchPlaceholder
                  }
                />
              </Container>
            ) : undefined}
          </Col>
        </Row>
        <Row align={"center"}>
          <Col lg={50} md={100} sm={100}>
            {filters}
          </Col>
          <Col lg={50} md={100} sm={100}>
            <Container
              align={"center"}
              display={"flex"}
              justify={"end"}
              scroll={"none"}
            >
              {columnToggle ? <ToggleFunction table={table} /> : undefined}
              {exportCsv ? (
                <CSVLink
                  data={flattenData(data as object[])}
                  filename={csvName}
                >
                  <Button variant={"ghost"}>
                    <Text bright={3}>
                      <FontAwesomeIcon icon={faFileExport} />
                      &nbsp;
                      {t("group.findings.exportCsv.text")}
                    </Text>
                  </Button>
                </CSVLink>
              ) : undefined}
              {extraButtons}
            </Container>
          </Col>
        </Row>
        {enableColumnFilters ? <Filters table={table} /> : undefined}
      </Container>
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
      {table.getFilteredRowModel().rows.length > 10 ? (
        <Pagination
          onNextPage={onNextPage}
          size={size ?? table.getFilteredRowModel().rows.length}
          table={table}
        />
      ) : undefined}
    </div>
  );
};

export { Table };
