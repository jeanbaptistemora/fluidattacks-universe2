/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type {
  Cell,
  Column,
  ColumnDef,
  ColumnFiltersState,
  InitialTableState,
  PaginationState,
  Row,
  RowData,
  SortingState,
  Table,
  VisibilityState,
} from "@tanstack/react-table";
import type { Dispatch, FormEvent, SetStateAction } from "react";

interface ICellHelper<TData extends RowData> {
  table: Table<TData>;
  column: Column<TData, unknown>;
  row: Row<TData>;
  cell: Cell<TData, unknown>;
  getValue: <TTValue = unknown>() => TTValue;
  renderValue: <TTValue = unknown>() => TTValue | null;
}

interface IPagMenuProps<TData extends RowData> {
  table: Table<TData>;
}

interface ITableProps<TData extends RowData> {
  csvName?: string;
  data: TData[];
  columnFilterSetter?: Dispatch<SetStateAction<ColumnFiltersState>>;
  columnFilterState?: ColumnFiltersState;
  columnToggle?: boolean;
  columnVisibilitySetter?: Dispatch<SetStateAction<VisibilityState>>;
  columnVisibilityState?: VisibilityState;
  columns: ColumnDef<TData>[];
  enableRowSelection?: boolean | ((row: Row<TData>) => boolean);
  enableColumnFilters?: boolean;
  enableSearchBar?: boolean;
  expandedRow?: (row: Row<TData>) => JSX.Element;
  exportCsv?: boolean;
  extraButtons?: JSX.Element;
  id: string;
  initState?: InitialTableState;
  onNextPage?: () => Promise<void>;
  onRowClick?: (row: Row<TData>) => (event: FormEvent<HTMLElement>) => void;
  onSearch?: (search: string) => void;
  paginationSetter?: Dispatch<SetStateAction<PaginationState>>;
  paginationState?: PaginationState;
  rowSelectionSetter?: Dispatch<SetStateAction<TData[]>>;
  rowSelectionState?: TData[];
  selectionMode?: "checkbox" | "radio";
  sortingSetter?: Dispatch<SetStateAction<SortingState>>;
  sortingState?: SortingState;
}

interface IToggleProps<TData extends RowData> {
  table: Table<TData>;
}

export type { ICellHelper, IPagMenuProps, ITableProps, IToggleProps };
