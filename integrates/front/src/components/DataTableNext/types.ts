/* eslint-disable @typescript-eslint/no-explicit-any
  --------
  Disabling this rule is necessary, because the dataset array may contain
  different types since this is a generic component.
*/
import type {
  BootstrapTableProps,
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

interface IFilterProps {
  defaultValue?: string;
  onChangeInput?: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onChangeSelect?: (event: React.ChangeEvent<HTMLSelectElement>) => void;
  rangeProps?: {
    defaultValue: { max: string; min: string };
    onChangeMax: (event: React.ChangeEvent<HTMLInputElement>) => void;
    onChangeMin: (event: React.ChangeEvent<HTMLInputElement>) => void;
    step: number;
  };
  selectOptions?: Record<string, number | string>;
  placeholder?: string;
  tooltipId: string;
  tooltipMessage: string;
  type: "date" | "number" | "range" | "select" | "text";
}

interface ICustomSearchProps {
  isCustomSearchEnabled: boolean;
  customSearchDefault: string;
  onUpdateCustomSearch: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

interface ICustomFiltersProps {
  customFiltersProps: IFilterProps[];
  isCustomFilterEnabled: boolean;
  onUpdateEnableCustomFilter: () => void;
}

interface ITableProps {
  bodyContainer?: string;
  bordered: boolean;
  columnToggle?: boolean;
  csvFilename?: string;
  customSearch?: ICustomSearchProps;
  dataset: any[];
  defaultSorted?: { dataField: string; order: SortOrder };
  expandRow?: BootstrapTableProps["expandRow"];
  exportCsv: boolean;
  extraButtons?: JSX.Element;
  customFilters?: ICustomFiltersProps;
  headerContainer?: string;
  headers: IHeaderConfig[];
  id: string;
  isFilterEnabled?: boolean;
  onPageChange?: (arg1: number) => void;
  // eslint-disable-next-line @typescript-eslint/no-magic-numbers
  pageSize: number;
  rowEvents?: Record<string, unknown>;
  search: boolean;
  selectionMode?: ISelectRowProps;
  striped?: boolean;
  onColumnToggle?: (arg1: string) => void;
  onUpdateEnableFilter?: () => void;
}

interface IHeaderConfig extends Omit<ColumnDescription, "text" | "width"> {
  dataField: string;
  header: string;
  visible?: boolean;
  width?: string;
  wordBreak?: "break-all" | "break-word" | "keep-all" | "normal";
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
  preferredPageSize: number;
  onSizePerPageChange?: (sizePerPage: number, page: number) => void;
  tableProps: ITableProps;
  toolkitProps: ToolkitContextType;
}

export {
  ICustomFiltersProps,
  ICustomSearchProps,
  ICustomToggleProps,
  IFilterProps,
  IHeaderConfig,
  ISelectRowProps,
  ITableProps,
  ITableWrapperProps,
};
