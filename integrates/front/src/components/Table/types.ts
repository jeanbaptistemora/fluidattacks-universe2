/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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

import type { ITableContainerProps } from "./styles";

interface ISelectRowProps extends Omit<SelectRowProps<any>, "onSelectAll"> {
  onSelectAll?: (
    isSelect: boolean,
    rows: any[],
    e: React.SyntheticEvent
    // eslint-disable-next-line @typescript-eslint/no-invalid-void-type
  ) => string[] | void;
}

interface IFilterProps {
  defaultValue?: string;
  onChangeInput?: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onChangeSelect?: (event: React.ChangeEvent<HTMLSelectElement>) => void;
  rangeProps?: {
    defaultValue: { max: string; min: string };
    onChangeMax: (event: React.ChangeEvent<HTMLInputElement>) => void;
    onChangeMin: (event: React.ChangeEvent<HTMLInputElement>) => void;
    step?: number;
  };
  selectOptions?: Record<string, number | string>;
  omit?: boolean;
  placeholder?: string;
  tooltipId: string;
  tooltipMessage: string;
  translateSelectOptions?: boolean;
  type: "date" | "dateRange" | "number" | "range" | "select" | "text";
}

interface ICustomSearchProps {
  isCustomSearchEnabled: boolean;
  customSearchDefault: string;
  onUpdateCustomSearch: (event: React.ChangeEvent<HTMLInputElement>) => void;
  position?: "left" | "right";
}

interface ICustomFiltersProps {
  customFiltersProps: IFilterProps[];
  hideResults?: boolean;
  isCustomFilterEnabled: boolean;
  onUpdateEnableCustomFilter: () => void;
  resultSize?: {
    current: number;
    total: number;
  };
}

interface IEditorProps {
  defaulValue: string;
  style: string;
  className: string;
  onKeyDown: () => void;
  onBlur: () => void;
  onUpdate: () => void;
}

interface ITableProps {
  clearFiltersButton?: () => void;
  columnToggle?: boolean;
  csvFilename?: string;
  customSearch?: ICustomSearchProps;
  dataset: any[];
  defaultSorted?: { dataField: string; order: SortOrder };
  expandRow?: BootstrapTableProps["expandRow"];
  exportCsv: boolean;
  extraButtons?: JSX.Element;
  extraButtonsRight?: JSX.Element;
  customFilters?: ICustomFiltersProps;
  headers: IHeaderConfig[];
  id: string;
  isFilterEnabled?: boolean;
  pageSize: number;
  rowEvents?: Record<string, unknown>;
  rowSize?: ITableContainerProps["rowSize"];
  search: boolean;
  selectionMode?: ISelectRowProps;
  onColumnToggle?: (arg1: string) => void;
  onUpdateEnableFilter?: () => void;
}

interface IHeaderConfig extends Omit<ColumnDescription, "text" | "width"> {
  dataField: string;
  header: string;
  omit?: boolean;
  nonToggleList?: boolean;
  visible?: boolean;
  width?: string;
  wordBreak?: "break-all" | "break-word" | "keep-all" | "normal";
  wrapped?: boolean;
  approveFunction?: (arg1?: Record<string, string>) => void;
  changeFunction?: (arg1: Readonly<Record<string, string>>) => void;
  deleteFunction?: (arg1?: Record<string, string>) => void;
  editFunction?: (arg1?: Record<string, string>) => void;
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

export type {
  ICustomFiltersProps,
  ICustomSearchProps,
  ICustomToggleProps,
  IEditorProps,
  IFilterProps,
  IHeaderConfig,
  ISelectRowProps,
  ITableProps,
  ITableWrapperProps,
};
