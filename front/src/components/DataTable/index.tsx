/* tslint:disable jsx-no-multiline-js jsx-no-lambda
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically creates the columns
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 */
import _ from "lodash";
import React, { ReactElement } from "react";
import { DropdownButton, Label, MenuItem } from "react-bootstrap";
import {
  BootstrapTable,
  DataAlignType,
  SearchField,
  SearchFieldProps,
  SelectRowMode,
  SizePerPageFunctionProps,
  TableHeaderColumn,
} from "react-bootstrap-table";
/* tslint:disable-next-line:no-import-side-effect no-submodule-imports
 * Disabling this two rules is necessary for
 * allowing the import of default styles that ReactTable needs
 * to display properly even if some of them are overridden later
 */
import "react-bootstrap-table/dist/react-bootstrap-table.min.css";
import globalStyle from "../../styles/global.css";
import translate from "../../utils/translations/translate";
import { Button } from "../Button";
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
  selectionMode: SelectRowMode;
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
  visible?: boolean;
  width?: string;
  wrapped?: boolean;

  approveFunction?(arg1: { [key: string]: string } | undefined): void;
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
        className={style.label}
        style={{
          backgroundColor: bgColor,
        }}
      >
        {value}
      </Label>
    );
};

export const dateFormatter: ((value: string) => string) =
  (value: string): string => {
  if (value.indexOf(":") !== -1) {

    return value.split(" ")[0];
  }

  return value;
};

const approveFormatter: ((value: string, row: { [key: string]: string }, key: IHeader) => JSX.Element) =
  (value: string, row: { [key: string]: string }, key: IHeader): JSX.Element =>
    (
      <a onClick={(): void => { if (key.approveFunction !== undefined) { key.approveFunction(row); }}}>
        <FluidIcon icon="ok" width="20px" height="20px" />
      </a>
    );

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
                          (key.approveFunction !== undefined ? approveFormatter :
                            undefined)))
      }
      formatExtraData={key}
      dataSort={true}
      hidden={
        (key.visible) === undefined ? key.visible : !key.visible}
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
          hidden={key === "uniqueId" ? true : false}
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

export const dataTable: React.FunctionComponent<ITableProps> = (props: ITableProps): JSX.Element => {
  const exportBtn: ((onClick: (e: React.MouseEvent<{}>) => void) => JSX.Element) =
    (onClick: (e: React.MouseEvent<{}>) => void): JSX.Element => (
      <Button onClick={onClick}><FluidIcon icon="export" />
        &nbsp;{translate.t("project.findings.exportCsv")}
      </Button>
    );

  const searchBar: ((searchProps: SearchFieldProps) => JSX.Element) = (searchProps: SearchFieldProps): JSX.Element => (
    <SearchField {...searchProps} className={style.searchBar} />
  );

  const pageSizeDropDown: ((dropDownProps: SizePerPageFunctionProps) => JSX.Element) =
    (dropDownProps: SizePerPageFunctionProps): JSX.Element => {

      const { changeSizePerPage, sizePerPageList } = dropDownProps;

      const handleSelect: ((select: {}) => void) = (select: {}): void => { changeSizePerPage(select as number); };

      return (
        <div>
          <DropdownButton title={dropDownProps.currSizePerPage} id="pageSizeDropDown" onSelect={handleSelect}>
            {(sizePerPageList as number[]).map((value: number, index: number): JSX.Element => (
              <MenuItem key={index} eventKey={value}>{value}</MenuItem>
            ))}
          </DropdownButton>
        </div>
      );
    };

  let dataset: Array<{}>;
  if (!_.isEmpty(props.dataset) && props.dataset.length > 0) {
    dataset = props.dataset.map((data: {uniqueId: number}, index: number) => {
      data.uniqueId = index;

      return data;
    });
  } else {
    dataset = [];
  }

  return (
    <React.StrictMode>
      <div id={props.id}>
        {
          _.isEmpty(dataset) && _.isEmpty(props.headers)
          ? <div/>
            : <div>
              {_.isEmpty(props.title) ? undefined : <h3 className={globalStyle.title}>{props.title}</h3>}
              <BootstrapTable
                data={dataset}
                exportCSV={props.exportCsv}
                keyField={
                    !_.isEmpty(dataset) && dataset.length > 0
                    ? "uniqueId"
                    : "_"
                }
                hover={true}
                options={{
                  exportCSVBtn: exportBtn,
                  onRowClick: (row: string): void => {
                    if (props.onClickRow !== undefined) { props.onClickRow(row); }
                  },
                  searchField: searchBar,
                  sizePerPage: props.pageSize,
                  sizePerPageDropDown: pageSizeDropDown,
                }}
                pagination={!_.isEmpty(dataset) && dataset.length > props.pageSize}
                search={props.search}
                selectRow={
                  props.enableRowSelection
                  ? {
                      clickToSelect: true,
                      mode: props.selectionMode,
                    }
                  : undefined
                }
                striped={props.striped}
                tableContainerClass={props.tableContainer === undefined ? undefined : props.tableContainer}
                headerContainerClass={props.headerContainer === undefined ? undefined : props.headerContainer}
                bodyContainerClass={props.bodyContainer === undefined ? undefined : props.bodyContainer}
                tableHeaderClass={props.tableHeader === undefined ? style.tableHeader : props.tableHeader}
                tableBodyClass={props.tableBody === undefined ? style.tableBody : props.tableBody}
              >
                {renderHeaders(props)}
              </BootstrapTable>
            </div>
        }
      </div>
    </React.StrictMode>
  );
};

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
