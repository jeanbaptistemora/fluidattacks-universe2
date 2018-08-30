/* tslint:disable jsx-no-multiline-js
 * Disabling this rule is necessary for the sake of
 * readability of the code that dynamically creates the columns
 */
import PropTypes from "prop-types";
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
import style from "./index.css";

interface ITableProps {
  /* tslint:disable-next-line:no-any
   * Disabling this rule is necessary because the dataset
   * array may contain different types since this is a
   * generic component
   */
  dataset: any[];
  exportCsv: boolean;
  headers: IHeader[];
  pageSize: number;
  search?: boolean;
  title: string;
  onClickRow(arg1: string | undefined): void;
}

interface IHeader {
  align?: DataAlignType;
  dataField: string;
  header: string;
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

const dataTable: React.StatelessComponent<ITableProps> =
  (props: ITableProps): JSX.Element => (
    <React.StrictMode>
      <div>
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
            props.headers.length > 0 ?
            props.headers.map((key: IHeader, i: number) =>
             (
              <TableHeaderColumn
                className={style.th}
                dataAlign={key.align}
                dataField={key.dataField}
                dataFormat={
                 key.isStatus ? statusFormatter :
                                (value: string): string => value
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
             )) :
            Object.keys(props.dataset[0])
            .map((key: string, i: number) =>
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
          }
        </BootstrapTable>
      </div>
    </React.StrictMode>
  );

dataTable.propTypes = {
  dataset: PropTypes.any,
  onClickRow: PropTypes.func,
  pageSize: PropTypes.number,
  title: PropTypes.string,
};

dataTable.defaultProps = {
  dataset: [{}],
  exportCsv: false,
  headers: [],
  onClickRow: (arg1: string): void => undefined,
  pageSize: 25,
  search: false,
};

export = dataTable;
