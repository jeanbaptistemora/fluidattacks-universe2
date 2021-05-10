/* eslint-disable @typescript-eslint/no-explicit-any
  --------
  Disabling this rule is necessary, because the dataset array may contain
  different types since this is a generic component.
*/
import type {
  ColumnDescription,
  SelectRowProps,
  SortOrder,
} from "react-bootstrap-table-next";
import type { ToolkitContextType } from "react-bootstrap-table2-toolkit";

interface ISelectRowProps extends Omit<SelectRowProps<any>, "onSelectAll"> {
  onSelectAll?: (
    isSelect: boolean,
    rows: any[],
    e: React.SyntheticEvent
  ) => string[];
}

interface ITableProps {
  bodyContainer?: string;
  bordered: boolean;
  columnToggle?: boolean;
  csvFilename?: string;
  dataset: any[];
  defaultSorted?: { dataField: string; order: SortOrder };
  exportCsv: boolean;
  extraButtons?: JSX.Element;
  headerContainer?: string;
  headers: IHeaderConfig[];
  id: string;
  isFilterEnabled?: boolean;
  numPages?: number;
  onSizePerPageChange?: (sizePerPage: number, page: number) => void;
  onPageChange?: (arg1: number) => void;
  pageSize: number;
  rowEvents?: Record<string, unknown>;
  search: boolean;
  selectionMode?: ISelectRowProps;
  striped?: boolean;
  tableBody?: string;
  tableHeader?: string;
  tableSize?: string;
  onColumnToggle?: (arg1: string) => void;
  onUpdateEnableFilter?: () => void;
}

interface IHeaderConfig extends Omit<ColumnDescription, "text" | "width"> {
  dataField: string;
  header: string;
  visible?: boolean;
  width?: string;
  wrapped?: boolean;
  approveFunction?: (arg1?: Record<string, string>) => void;
  changeFunction?: (arg1: Readonly<Record<string, string>>) => void;
  deleteFunction?: (arg1?: Record<string, string>) => void;
  onSort?: (dataField: string, order: SortOrder) => void;
}

interface ICustomToggleProps {
  propsTable: ITableProps;
  propsToggle: ToolkitContextType["columnToggleProps"];
}

interface ITableWrapperProps {
  dataset: Record<string, unknown>[];
  extraButtons?: JSX.Element;
  tableProps: ITableProps;
  toolkitProps: ToolkitContextType;
}

export {
  ICustomToggleProps,
  IHeaderConfig,
  ISelectRowProps,
  ITableProps,
  ITableWrapperProps,
};
