import type {
  Cell,
  Column,
  ColumnDef,
  InitialTableState,
  Row,
  Table,
} from "@tanstack/react-table";
import type { Dispatch, FormEvent, SetStateAction } from "react";

interface ICellHelper<TData> {
  table: Table<TData>;
  column: Column<TData, unknown>;
  row: Row<TData>;
  cell: Cell<TData, unknown>;
  getValue: <TTValue = unknown>() => TTValue;
  renderValue: <TTValue = unknown>() => TTValue | null;
}

interface IPagMenuProps<TData> {
  table: Table<TData>;
}

interface ITableProps<TData> {
  csvName?: string;
  data: TData[];
  columns: ColumnDef<TData>[];
  columnToggle?: boolean;
  enableRowSelection?: boolean;
  enableSearchBar?: boolean;
  expandedRow?: (row: Row<TData>) => JSX.Element;
  exportCsv?: boolean;
  extraButtons?: JSX.Element;
  id: string;
  initState?: InitialTableState;
  onRowClick?: (row: Row<TData>) => (event: FormEvent<HTMLElement>) => void;
  rowSelectionSetter?: Dispatch<SetStateAction<TData[]>>;
}

interface IToggleProps<TData> {
  table: Table<TData>;
}

export type { ICellHelper, IPagMenuProps, ITableProps, IToggleProps };
