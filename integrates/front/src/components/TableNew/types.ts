import type { ColumnDef, Row, Table } from "@tanstack/react-table";
import type { FormEvent } from "react";

interface IPagMenuProps<TData> {
  table: Table<TData>;
}

interface ITableProps<TData> {
  id: string;
  data: TData[];
  columns: ColumnDef<TData>[];
  columnToggle?: boolean;
  exportCsv?: boolean;
  extraButtons?: JSX.Element;
  csvName?: string;
  showPagination?: boolean;
  onRowClick?: (row: Row<TData>) => (event: FormEvent<HTMLElement>) => void;
}

interface IToggleProps<TData> {
  id: string;
  table: Table<TData>;
}

export type { IPagMenuProps, ITableProps, IToggleProps };
