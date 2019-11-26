/* tslint:disable jsx-no-multiline-js no-any
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically creates the columns
 * NO-ANY: Disabling this rule is necessary because the dataset
 * array may contain different types since this is a
 * generic component
 */
import _ from "lodash";
import React from "react";
import BootstrapTable, { Column } from "react-bootstrap-table-next";
/* tslint:disable-next-line:no-import-side-effect no-submodule-imports
* Disabling this two rules is necessary for
* allowing the import of default styles that ReactTable needs
* to display properly even if some of them are overridden later
*/
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";
import filterFactory from "react-bootstrap-table2-filter";
import paginationFactory from "react-bootstrap-table2-paginator";
import globalStyle from "../../styles/global.css";
import { FluidIcon } from "../FluidIcon";
import style from "./index.css";
import { IHeader, ITableProps } from "./types";

const dateFormatter: ((value: string) => string) =
  (value: string): string => {
  if (value.indexOf(":") !== -1) {

    return value.split(" ")[0];
  }

  return value;
};

const approveFormatter: ((value: string, row: { [key: string]: string }, rowIndex: number, key: IHeader)
=> JSX.Element) =
  (value: string, row: { [key: string]: string }, rowIndex: number, key: IHeader): JSX.Element => {
    const handleApproveFormatter: (() => void) = (): void => {
      if (key.approveFunction !== undefined) {
        key.approveFunction(row);
      }
    };

    return (
      <a onClick={handleApproveFormatter}>
        <FluidIcon icon="verified" width="20px" height="20px" />
      </a>
    );
  };

const deleteFormatter: ((value: string, row: { [key: string]: string }, rowIndex: number, key: IHeader)
=> JSX.Element) =
  (value: string, row: { [key: string]: string }, rowIndex: number, key: IHeader): JSX.Element => {
    const handleDeleteFormatter: (() => void) = (): void => {
      if (key.deleteFunction !== undefined) {
        key.deleteFunction(row);
      }
    };

    return (
      <a onClick={handleDeleteFormatter}>
        <FluidIcon icon="delete" width="20px" height="20px" />
      </a>
    );
  };

const renderGivenHeaders: ((arg1: IHeader[], columnHeaderStyle?: string) => Column[]) =
  (headers: IHeader[], columnHeaderStyle?: string): Column[] => (headers.map((key: IHeader, index: number) =>
   ({
      align: key.align,
      dataField: key.dataField,
      filter: key.filter,
      formatExtraData: key,
      formatter: key.isDate ? dateFormatter :
        (key.deleteFunction !== undefined ? deleteFormatter :
          (key.approveFunction !== undefined ? approveFormatter : undefined)),
      headerClasses: columnHeaderStyle,
      headerStyle: (): any => ({ width: key.width }),
      hidden: (key.visible) === undefined ? key.visible : !key.visible,
      sort: true,
      text: key.header,
    }
    ))
  );

const renderDynamicHeaders: ((arg1: string[]) => Column[]) =
  (dataFields: string[]): Column[] => (
    dataFields.map((key: string, index: number) =>
      ({
          dataField: key,
          headerStyle: (): any => ({ width: dataFields.length > 10 ? "150px" : undefined }),
          hidden: key === "uniqueId" ? true : false,
          sort: true,
          text: key,
      }
    ))
  );

const renderHeaders: ((arg1: ITableProps) => Column[]) =
  (props: ITableProps): Column[] => (
    props.headers.length > 0 ?
    renderGivenHeaders(props.headers, props.tableHeader) :
    renderDynamicHeaders(Object.keys(props.dataset[0]))
  );

export const dataTableNext: React.FunctionComponent<ITableProps> = (props: ITableProps): JSX.Element => {

  let dataset: Array<{}>;
  if (!_.isEmpty(props.dataset) && props.dataset.length > 0) {
    dataset = props.dataset.map((data: {uniqueId: number}, index: number) => {
      data.uniqueId = index;

      return data;
    });
  } else {
    dataset = [];
  }
  const paginationOptions: PaginationProps = {
    sizePerPage: props.pageSize,
  };
  const handleTableChange: ((type: TableChangeType, newState: TableChangeNewState) => void) =
  (type: TableChangeType, newState: TableChangeNewState): void => {
    if (props.onTableChange !== undefined) {
      props.onTableChange(type, newState);
    }
  };

  return (
    <React.StrictMode>
      <div id={props.id}>
        {
          _.isEmpty(dataset) && _.isEmpty(props.headers)
          ? <div/>
            : <div>
              {_.isEmpty(props.title) ? undefined : <h3 className={globalStyle.title}>{props.title}</h3>}
              <BootstrapTable
                bordered={props.bordered}
                data={dataset}
                keyField={
                    !_.isEmpty(dataset) && dataset.length > 0
                    ? "uniqueId"
                    : "_"
                }
                columns={renderHeaders(props)}
                filter={filterFactory()}
                hover={true}
                onTableChange={handleTableChange}
                pagination={!_.isEmpty(dataset) && dataset.length > props.pageSize ?
                  paginationFactory(paginationOptions) : undefined}
                remote={props.remote}
                rowClasses={props.tableBody === undefined ? style.tableBody : props.tableBody}
              />
            </div>
        }
      </div>
    </React.StrictMode>
  );
};

dataTableNext.defaultProps = {
  bodyContainer: undefined,
  enableRowSelection: false,
  exportCsv: false,
  headerContainer: undefined,
  headers: [],
  onClickRow: (arg1: string): void => undefined,
  onTableChange: (type: TableChangeType, newState: TableChangeNewState): void => undefined,
  pageSize: 25,
  remote: {
    cellEdit: false,
    filter: true,
    pagination: false,
    sort: false,
  },
  search: false,
  tableBody: undefined,
  tableHeader: undefined,
};

export { dataTableNext as DataTableNext };
