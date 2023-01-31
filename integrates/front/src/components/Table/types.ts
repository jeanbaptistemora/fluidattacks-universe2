import type {
  Cell,
  Column,
  ColumnDef,
  ColumnFiltersState,
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
  filters?: JSX.Element;
  id: string;
  onNextPage?: () => Promise<void>;
  onRowClick?: (row: Row<TData>) => (event: FormEvent<HTMLElement>) => void;
  onSearch?: (search: string) => void;
  rowSelectionSetter?: Dispatch<SetStateAction<TData[]>>;
  rowSelectionState?: TData[];
  selectionMode?: "checkbox" | "radio";
  searchPlaceholder?: string;
  size?: number;
  sortingSetter?: Dispatch<SetStateAction<SortingState>>;
  sortingState?: SortingState;
}

interface IToggleProps<TData extends RowData> {
  table: Table<TData>;
}

export type { ICellHelper, IPagMenuProps, ITableProps, IToggleProps };
