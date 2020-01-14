/* tslint:disable no-any
 * NO-ANY: Disabling this rule is necessary because the dataset
 * array may contain different types since this is a generic component
 */
import { ReactElement } from "react";
import { ColumnToggleProps } from "react-bootstrap-table2-toolkit";

export interface ITableProps {
  bodyContainer?: string;
  bordered: boolean;
  columnToggle?: boolean;
  dataset: any[];
  defaultSorted?: Sorted;
  exportCsv: boolean;
  headerContainer?: string;
  headers: IHeader[];
  id: string;
  isFilterEnabled?: boolean;
  pageSize: number;
  remote: RemoteProps | boolean;
  rowEvents?: {};
  search: boolean;
  selectionMode?: SelectRowOptions;
  striped?: boolean;
  tableBody?: string;
  tableHeader?: string;
  title?: string;
  onClickRow?(arg1: string | {} | undefined): void;
  onColumnToggle?(arg1: string): void;
  onTableChange?(type: TableChangeType, newState: TableChangeNewState): void;
  onUpdateEnableFilter?(): void;
}

export interface IHeader {
  align?: string;
  dataField: string;
  filter?: any;
  header: string;
  visible?: boolean;
  width?: string;
  wrapped?: boolean;

  approveFunction?(arg1: { [key: string]: string } | undefined): void;
  changeFunction?(arg1: { [key: string]: string } | undefined): void;
  deleteFunction?(arg1: { [key: string]: string } | undefined): void;
  formatter?(value: string, row: any, rowIndex: number, formatExtraData: any): string | ReactElement;
  onSort?(dataField: string, order: SortOrder): void;
}

export interface ICustomToggle {
  propsTable: ITableProps;
  propsToggle: ColumnToggleProps;
}
