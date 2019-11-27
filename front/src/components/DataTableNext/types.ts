/* tslint:disable no-any
 * NO-ANY: Disabling this rule is necessary because the dataset
 * array may contain different types since this is a generic component
 */
import { ReactElement } from "react";

export interface ITableProps {
  bodyContainer?: string;
  bordered: boolean;
  dataset: any[];
  enableRowSelection: boolean;
  exportCsv: boolean;
  headerContainer?: string;
  headers: IHeader[];
  id: string;
  pageSize: number;
  remote: RemoteProps;
  search?: boolean;
  selectionMode?: SelectRowOptions;
  tableBody?: string;
  tableHeader?: string;
  title?: string;
  onClickRow?(arg1: string | {} | undefined): void;
  onTableChange?(type: TableChangeType, newState: TableChangeNewState): void;
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
}
