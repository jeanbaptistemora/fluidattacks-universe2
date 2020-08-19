/* eslint-disable @typescript-eslint/no-explicit-any
  --------
  Disabling this rule is necessary, because the dataset array may contain
  different types since this is a generic component.
*/
import { Column } from "react-bootstrap-table-next";
import { ReactElement } from "react";
import {
  ColumnToggleProps,
  ToolkitProviderProps,
} from "react-bootstrap-table2-toolkit";

interface ITableProps {
  bodyContainer?: string;
  bordered: boolean;
  columnToggle?: boolean;
  csvFilename?: string;
  dataset: any[];
  defaultSorted?: Sorted;
  exportCsv: boolean;
  headerContainer?: string;
  headers: IHeaderConfig[];
  id: string;
  isFilterEnabled?: boolean;
  pageSize: number;
  rowEvents?: Record<string, unknown>;
  search: boolean;
  selectionMode?: SelectRowOptions;
  striped?: boolean;
  tableBody?: string;
  tableHeader?: string;
  onColumnToggle?: (arg1: string) => void;
  onUpdateEnableFilter?: () => void;
}

interface IHeaderConfig {
  align?: string;
  dataField: string;
  filter?: unknown;
  header: string;
  visible?: boolean;
  width?: string;
  wrapped?: boolean;
  approveFunction?: (arg1?: Record<string, string>) => void;
  changeFunction?: (arg1: Readonly<Record<string, string>>) => void;
  deleteFunction?: (arg1?: Record<string, string>) => void;
  formatter?: (
    cell: any,
    row: any,
    rowIndex: number,
    formatExtraData: any
  ) => string | ReactElement;
  onSort?: (dataField: string, order: SortOrder) => void;
  sortFunc?: (
    a: any,
    b: any,
    order: "asc" | "desc",
    rowA: any,
    rowB: any
  ) => number;
  headerFormatter?: (
    column: Column,
    colIndex: number,
    components: Record<string, ReactElement>
  ) => JSX.Element;
}

interface ICustomToggleProps {
  propsTable: ITableProps;
  propsToggle: ColumnToggleProps;
}

interface ITableWrapperProps {
  dataset: Record<string, unknown>[];
  tableProps: ITableProps;
  toolkitProps: ToolkitProviderProps;
}

export { ITableProps, IHeaderConfig, ICustomToggleProps, ITableWrapperProps };
