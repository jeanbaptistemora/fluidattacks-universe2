import _ from "lodash";
import React, { ReactElement } from "react";
import { DropdownButton, MenuItem } from "react-bootstrap";
import BootstrapTable, { Column } from "react-bootstrap-table-next";
/* tslint:disable-next-line:no-import-side-effect no-submodule-imports
* Disabling this two rules is necessary for
* allowing the import of default styles that ReactTable needs
* to display properly even if some of them are overridden later
*/
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";
import filterFactory from "react-bootstrap-table2-filter";
import paginationFactory from "react-bootstrap-table2-paginator";
import { default as globalStyle } from "../../styles/global.css";
import { default as style } from "./index.css";
import { IHeader, ITableProps } from "./types";

const handleFormatter: ((value: string, row: { [key: string]: string }, rowIndex: number, key: IHeader)
=> string | ReactElement | undefined) =
(value: string, row: { [key: string]: string }, rowIndex: number, key: IHeader): string | ReactElement | undefined => {
  if (key.formatter !== undefined) {
    return key.formatter(value, row, rowIndex, key);
  }
};

const renderGivenHeaders: ((arg1: IHeader[], columnHeaderStyle?: string) => Column[]) =
  (headers: IHeader[], columnHeaderStyle?: string): Column[] => (headers.map((key: IHeader) => {
    const isFormatter: boolean = key.formatter !== undefined;

    return {
      align: key.align,
      dataField: key.dataField,
      filter: key.filter,
      formatExtraData: key,
      formatter: isFormatter ? handleFormatter : undefined,
      headerClasses: columnHeaderStyle,
      headerStyle: (): {} => ({ width: key.width }),
      hidden: (key.visible) === undefined ? key.visible : !key.visible,
      sort: true,
      text: key.header,
    };
  })
);

const renderDynamicHeaders: ((arg1: string[]) => Column[]) =
  (dataFields: string[]): Column[] => (
    dataFields.map((key: string, index: number) =>
      ({
          dataField: key,
          headerStyle: (): {} => ({ width: dataFields.length > 10 ? "150px" : undefined }),
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

const renderTable: ((props: ITableProps, dataset: Array<{}>) => JSX.Element) =
  (props: ITableProps, dataset: Array<{}>): JSX.Element => {

    const sizePerPageRenderer: ((renderer: SizePerPageRenderer) => JSX.Element) =
    (renderer: SizePerPageRenderer): JSX.Element => {
      const { options, currSizePerPage, onSizePerPageChange} = renderer;
      const handleSelect: ((select: {}) => void) = (select: {}): void => {
        onSizePerPageChange(select as number);
      };
      const renderMenuItems: ((value: {page: number; text: string}, index: number) => JSX.Element) =
      (value: {page: number; text: string}, index: number): JSX.Element => (
          <MenuItem key={index} eventKey={value.page}>{value.page}</MenuItem>
        );

      return (
        <div>
          <DropdownButton title={currSizePerPage} id="pageSizeDropDown" onSelect={handleSelect}>
            {options.map(renderMenuItems)}
          </DropdownButton>
        </div>
      );
    };
    const paginationOptions: PaginationProps = {
      sizePerPage: props.pageSize,
      sizePerPageRenderer,
    };
    const handleTableChange: ((type: TableChangeType, newState: TableChangeNewState) => void) =
    (type: TableChangeType, newState: TableChangeNewState): void => {
      if (props.onTableChange !== undefined) {
        props.onTableChange(type, newState);
      }
    };
    const isPaginationEnable: boolean = !_.isEmpty(dataset) && dataset.length > props.pageSize;

    return (
      <div>
        {_.isEmpty(props.title) ? undefined : <h3 className={globalStyle.title}>{props.title}</h3>}
        <BootstrapTable
          bordered={props.bordered}
          data={dataset}
          keyField={!_.isEmpty(dataset) && dataset.length > 0 ? "uniqueId" : "_"}
          columns={renderHeaders(props)}
          filter={filterFactory()}
          hover={true}
          onTableChange={handleTableChange}
          pagination={isPaginationEnable ? paginationFactory(paginationOptions) : undefined}
          remote={props.remote}
          rowClasses={props.tableBody === undefined ? style.tableBody : props.tableBody}
        />
      </div>
    );
  };

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

  return (
    <React.StrictMode>
      <div id={props.id}>
        {_.isEmpty(dataset) && _.isEmpty(props.headers) ? <div/> : renderTable(props, dataset)}
      </div>
    </React.StrictMode>
  );
};

dataTableNext.defaultProps = {
  bodyContainer: undefined,
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
