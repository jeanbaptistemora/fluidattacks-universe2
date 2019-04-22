/* tslint:disable jsx-no-multiline-js jsx-no-lambda
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically creates the columns
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 */
import _ from "lodash";
import React, { ReactElement } from "react";
import { Label } from "react-bootstrap";
import {
  BootstrapTable,
  DataAlignType,
  TableHeaderColumn,
} from "react-bootstrap-table";
/* tslint:disable-next-line:no-import-side-effect no-submodule-imports
 * Disabling this two rules is necessary for
 * allowing the import of default styles that ReactTable needs
 * to display properly even if some of them are overridden later
 */
import "react-bootstrap-table/dist/react-bootstrap-table.min.css";
import globalStyle from "../../styles/global.css";
import { FluidIcon } from "../FluidIcon";
import style from "./index.css";

export interface ITableProps {
  bodyContainer?: string;
  /* tslint:disable-next-line:no-any
   * Disabling this rule is necessary because the dataset
   * array may contain different types since this is a
   * generic component
   */
  dataset: any[];
  enableRowSelection: boolean;
  exportCsv: boolean;
  headerContainer?: string;
  headers: IHeader[];
  id: string;
  pageSize: number;
  search?: boolean;
  striped?: boolean;
  tableBody?: string;
  tableContainer?: string;
  tableHeader?: string;
  title?: string;
  onClickRow?(arg1: string | {} | undefined): void;
}

export interface IHeader {
  align?: DataAlignType;
  dataField: string;
  header: string;
  isDate: boolean;
  isStatus: boolean;
  width?: string;
  wrapped?: boolean;
  deleteFunction?(arg1: { [key: string]: string } | undefined): void;
}

const statusFormatter: ((value: string) => ReactElement<Label>) =
  (value: string): ReactElement<Label> => {
    let bgColor: string;

    switch (value) {
      case "Cerrado":
      case "Closed":
      case "Tratada":
      case "Solved":
        bgColor = "#31c0be";
        break;
      case "Abierto":
      case "Open":
      case "Pendiente":
      case "Unsolved":
        bgColor = "#f22";
        break;
      case "Parcialmente cerrado":
      case "Partially closed":
        bgColor = "#ffbf00";
        break;
      default:
        bgColor = "";
    }

    return (
      <Label
        style={{
          backgroundColor: bgColor,
        }}
      >
        {value}
      </Label>
    );
};

const dateFormatter: ((value: string) => string) =
  (value: string): string => {
  if (value.indexOf(":") !== -1) {

    return value.split(" ")[0];
  }

  return value;
};

const deleteFormatter: ((value: string, row: { [key: string]: string }, key: IHeader) => JSX.Element) =
  (value: string, row: { [key: string]: string }, key: IHeader): JSX.Element =>
    (
      <a onClick={(): void => { if (key.deleteFunction !== undefined) { key.deleteFunction(row); }}}>
        <FluidIcon icon="delete" width="20px" height="20px" />
      </a>
    );

const renderGivenHeaders: ((arg1: IHeader[]) => JSX.Element[]) =
  (headers: IHeader[]): JSX.Element[] => (
  headers.map((key: IHeader, index: number) =>
   (
    <TableHeaderColumn
      dataAlign={key.align}
      dataField={key.dataField}
      dataFormat={
       key.isStatus ? statusFormatter :
                      (key.isDate ? dateFormatter :
                        (key.deleteFunction !== undefined ? deleteFormatter :
                          undefined))
      }
      formatExtraData={key}
      dataSort={true}
      key={index}
      tdStyle={{
       textAlign: key.align,
       whiteSpace: key.wrapped === undefined ? "nowrap" :
       key.wrapped ? "unset" : "nowrap",
      }}
      width={key.width}
    >
      {key.header}
    </TableHeaderColumn>
   ))
);

const renderDynamicHeaders: ((arg1: string[]) => JSX.Element[]) =
  (dataFields: string[]): JSX.Element[] => (
  dataFields.map((key: string, index: number) =>
    (
      <TableHeaderColumn
        dataField={key}
        dataSort={true}
        key={index}
        width={dataFields.length > 10 ? "150px" : undefined}
        tdStyle={{
          whiteSpace: "unset",
        }}
      >
        {key}
      </TableHeaderColumn>
    ))
);

const renderHeaders: ((arg1: ITableProps) => JSX.Element[]) =
  (props: ITableProps): JSX.Element[] => (

  props.headers.length > 0 ?
  renderGivenHeaders(props.headers) :
  renderDynamicHeaders(Object.keys(props.dataset[0]))
);

export const dataTable: React.StatelessComponent<ITableProps> =
  (props: ITableProps): JSX.Element => (
    <React.StrictMode>
      <div id={props.id}>
        {
          _.isEmpty(props.dataset) && _.isEmpty(props.headers)
          ? <div/>
          : <div>
              {_.isEmpty(props.title) ? undefined : <h1 className={globalStyle.title}>{props.title}</h1>}
              <BootstrapTable
                data={props.dataset}
                exportCSV={props.exportCsv}
                keyField={
                    !_.isEmpty(props.dataset) && props.dataset.length > 0
                    ? Object.keys(props.dataset[0])[0]
                    : "_"
                }
                hover={true}
                options={{
                 onRowClick: (row: string): void => {
                   if (props.onClickRow !== undefined) { props.onClickRow(row); }
                 },
                 sizePerPage: props.pageSize,
                }}
                pagination={!_.isEmpty(props.dataset) && props.dataset.length > props.pageSize}
                search={props.search}
                selectRow={
                  props.enableRowSelection
                  ? {
                      clickToSelect: true,
                      mode: "radio",
                    }
                  : undefined
                }
                striped={props.striped}
                tableContainerClass={props.tableContainer === undefined ? undefined : props.tableContainer}
                headerContainerClass={props.headerContainer === undefined ? undefined : props.headerContainer}
                bodyContainerClass={props.bodyContainer === undefined ? undefined : props.bodyContainer}
                tableHeaderClass={props.tableHeader === undefined ? style.tableHeader : props.tableHeader}
                tableBodyClass={props.tableBody === undefined ? undefined : props.tableBody}
              >
                {renderHeaders(props)}
              </BootstrapTable>
            </div>
        }
      </div>
    </React.StrictMode>
  );

dataTable.defaultProps = {
  bodyContainer: undefined,
  enableRowSelection: false,
  exportCsv: false,
  headerContainer: undefined,
  headers: [],
  onClickRow: (arg1: string): void => undefined,
  pageSize: 25,
  search: false,
  striped: true,
  tableBody: undefined,
  tableContainer: undefined,
  tableHeader: undefined,
};
