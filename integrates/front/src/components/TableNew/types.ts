import type {
  Cell,
  Column,
  ColumnDef,
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
  id: string;
  data: TData[];
  columns: ColumnDef<TData>[];
  columnToggle?: boolean;
  expandedRow?: (row: Row<TData>) => JSX.Element;
  exportCsv?: boolean;
  extraButtons?: JSX.Element;
  csvName?: string;
  enableRowSelection?: false;
  enableSearchBar?: boolean;
  rowSelectionSetter?: undefined;
  showPagination?: boolean;
  onRowClick?: (row: Row<TData>) => (event: FormEvent<HTMLElement>) => void;
}

interface ITablepropsWithRowSel<TData>
  extends Omit<
    ITableProps<TData>,
    "enableRowSelection" | "rowSelectionSetter"
  > {
  enableRowSelection: true;
  rowSelectionSetter: Dispatch<SetStateAction<TData[]>>;
}

interface IToggleProps<TData> {
  id: string;
  table: Table<TData>;
}

export type {
  ICellHelper,
  IPagMenuProps,
  ITableProps,
  ITablepropsWithRowSel,
  IToggleProps,
};
