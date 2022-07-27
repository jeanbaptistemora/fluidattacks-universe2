import type { ColumnDef, Table } from "@tanstack/react-table";

interface IPagMenuProps<TData> {
  table: Table<TData>;
}

interface ITableProps<TData> {
  id: string;
  data: TData[];
  columns: ColumnDef<TData>[];
  columnToggle?: boolean;
  exportCsv?: boolean;
  csvName?: string;
  rowFunction?: () => void;
}

interface IToggleProps<TData> {
  id: string;
  table: Table<TData>;
}

export type { IPagMenuProps, ITableProps, IToggleProps };
