/* tslint:disable jsx-no-multiline-js
 * Disabling this rule is necessary for the sake of
 * readability of the code that dynamically creates the columns
 */
import PropTypes from "prop-types";
import React, { ReactElement } from "react";
import { Label, Radio } from "react-bootstrap";
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
import style from "./index.css";

interface ITableProps {
  /* tslint:disable-next-line:no-any
   * Disabling this rule is necessary because the dataset
   * array may contain different types since this is a
   * generic component
   */
  dataset: any[];
  enableRowSelection: boolean;
  exportCsv: boolean;
  headers: IHeader[];
  id: string;
  pageSize: number;
  search?: boolean;
  title: string;
  onClickRow(arg1: string | undefined): void;
}

interface IHeader {
  align?: DataAlignType;
  dataField: string;
  header: string;
  isDate: boolean;
  isStatus: boolean;
  width?: string;
  wrapped?: boolean;
}

const statusFormatter: ((value: string) => ReactElement<Label>) =
  (value: string): ReactElement<Label> => {
    let bgColor: string;

    switch (value) {
      case "Cerrado":
      case "Closed":
        bgColor = "#31c0be";
        break;
      case "Abierto":
      case "Open":
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

const selectFormatter: (() => ReactElement<Radio>) =
  (): ReactElement<Radio> => (
  <Radio
    name="selectRow"
  />
);

const renderGivenHeaders: ((arg1: IHeader[]) => JSX.Element[]) =
  (headers: IHeader[]): JSX.Element[] => (
  headers.map((key: IHeader, i: number) =>
   (
    <TableHeaderColumn
      className={style.th}
      dataAlign={key.align}
      dataField={key.dataField}
      dataFormat={
       key.isStatus ? statusFormatter :
                      (key.isDate ? dateFormatter :
                        (value: string): string => value)
      }
      dataSort={true}
      key={i}
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
  dataFields.map((key: string, i: number) =>
    (
      <TableHeaderColumn
        className={style.th}
        dataField={key}
        dataSort={true}
        key={i}
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

const dataTable: React.StatelessComponent<ITableProps> =
  (props: ITableProps): JSX.Element => (
    <React.StrictMode>
      <div id={props.id}>
        <h1 className={globalStyle.title}>{props.title}</h1>
        <BootstrapTable
          data={props.dataset}
          exportCSV={props.exportCsv}
          hover={true}
          keyField=" "
          options={{
           onRowClick: (row: string): void => {
             props.onClickRow(row);
           },
           sizePerPage: props.pageSize,
          }}
          pagination={props.dataset.length > props.pageSize}
          search={props.search}
          striped={true}
        >
          {
            props.enableRowSelection ?
            [
              <TableHeaderColumn
                className={style.th}
                key={0}
                dataField=""
                dataFormat={selectFormatter}
                width={"3%"}
              />,
            ].concat(renderHeaders(props))
            : renderHeaders(props)
          }
        </BootstrapTable>
      </div>
    </React.StrictMode>
  );

dataTable.propTypes = {
  dataset: PropTypes.any,
  enableRowSelection: PropTypes.bool,
  id: PropTypes.string,
  onClickRow: PropTypes.func,
  pageSize: PropTypes.number,
  title: PropTypes.string,
};

dataTable.defaultProps = {
  dataset: [{}],
  enableRowSelection: false,
  exportCsv: false,
  headers: [],
  onClickRow: (arg1: string): void => undefined,
  pageSize: 25,
  search: false,
};

export = dataTable;
