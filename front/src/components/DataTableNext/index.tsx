/* tslint:disable: jsx-no-multiline-js variable-name
 * VARIABLE-NAME: Disabling here is necessary due a conflict
 * between lowerCamelCase var naming rule from tslint
 * and PascalCase rule for naming JSX elements
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code in graphql queries
 */
import _ from "lodash";
import React from "react";
import { Col, DropdownButton, Glyphicon, MenuItem, Row } from "react-bootstrap";
import BootstrapTable from "react-bootstrap-table-next";
/* tslint:disable-next-line:no-import-side-effect no-submodule-imports
* Disabling this two rules is necessary for
* allowing the import of default styles that ReactTable needs
* to display properly even if some of them are overridden later
*/
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";
import filterFactory from "react-bootstrap-table2-filter";
import paginationFactory from "react-bootstrap-table2-paginator";
// tslint:disable-next-line:no-import-side-effect no-submodule-imports
import "react-bootstrap-table2-paginator/dist/react-bootstrap-table2-paginator.min.css";
import ToolkitProvider, { Search, ToolkitProviderProps } from "react-bootstrap-table2-toolkit";
// tslint:disable-next-line:no-import-side-effect no-submodule-imports
import "react-bootstrap-table2-toolkit/dist/react-bootstrap-table2-toolkit.min.css";
import { default as globalStyle } from "../../styles/global.css";
import translate from "../../utils/translations/translate";
import { Button } from "../Button";
import { TooltipWrapper } from "../TooltipWrapper/index";
import { CustomToggleList } from "./customToggleList";
import { ExportCSVButtonWrapper } from "./exportCSVButton";
import { default as style } from "./index.css";
import { ITableProps } from "./types";
import { customizeColumns } from "./utils";

const renderTable: ((toolkitProps: ToolkitProviderProps, props: ITableProps, dataset: Array<{}>) => JSX.Element) =
  (toolkitProps: ToolkitProviderProps, props: ITableProps, dataset: Array<{}>): JSX.Element => {

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
    const enableFilter: (() => JSX.Element) = (): JSX.Element => {
      const isEnableFilter: boolean = !_.isUndefined(props.isFilterEnabled) ? props.isFilterEnabled : true;
      const handleUpdateEnableFilter: (() => void) = (): void => {
        if (props.onUpdateEnableFilter !== undefined) {
          props.onUpdateEnableFilter();
        }
      };

      return (
        <TooltipWrapper message={translate.t("dataTableNext.tooltip")}>
          <Button onClick={handleUpdateEnableFilter} active={!isEnableFilter}>
            {isEnableFilter ? <Glyphicon glyph="minus"/> : <Glyphicon glyph="plus"/>}&nbsp;
            {translate.t("dataTableNext.filters")}
          </Button>
        </TooltipWrapper>
      );
    };
    const isPaginationEnable: boolean = !_.isEmpty(dataset) && dataset.length > props.pageSize;
    const { SearchBar } = Search;
    const handleNoData: (() => string) = (): string => (translate.t("dataTableNext.noDataIndication"));
    const columnToggle: boolean = !_.isUndefined(props.columnToggle) ? props.columnToggle : false;
    const displayEnableFilter: boolean = !_.isUndefined(props.isFilterEnabled) ? true : false;

    return (
      <div>
        <Row className={style.tableOptions}>
          <Col lg={3} md={3} sm={6} xs={12}>
          {props.exportCsv ? <ExportCSVButtonWrapper {...toolkitProps}/> : undefined}
          </Col>
          <Col lg={3} md={3} sm={6} xs={12}>
            {columnToggle ? <CustomToggleList propsToggle={toolkitProps.columnToggleProps} propsTable={props} />
             : undefined}
          </Col>
          <Col lg={3} md={3} sm={6} xs={12}>
            {displayEnableFilter ? enableFilter() : undefined}
          </Col>
          <Col lg={3} md={3} sm={6} xs={12}>
            {props.search ? <SearchBar {...toolkitProps.searchProps} className={style.searchBar} /> : undefined}
          </Col>
        </Row>
        <BootstrapTable
          {...toolkitProps.baseProps}
          bordered={props.bordered}
          defaultSorted={!_.isUndefined(props.defaultSorted) ? [props.defaultSorted] : undefined}
          filter={filterFactory()}
          headerClasses={props.tableHeader === undefined ? style.tableHeader : props.tableHeader}
          hover={true}
          onTableChange={handleTableChange}
          noDataIndication={handleNoData}
          pagination={isPaginationEnable ? paginationFactory(paginationOptions) : undefined}
          remote={props.remote}
          rowClasses={props.tableBody === undefined ? style.tableBody : props.tableBody}
          rowEvents={props.rowEvents}
          selectRow={props.selectionMode}
          striped={props.striped}
        />
      </div>
    );
  };

const renderToolKitProvider: ((props: ITableProps, dataset: Array<{}>) => JSX.Element) =
  (props: ITableProps, dataset: Array<{}>): JSX.Element => {
    const { columnToggle, csvFilename = "spreadsheet.csv", search, title } = props;

    return (
      <div>
      {_.isEmpty(title) ? undefined : <h3 className={globalStyle.title}>{title}</h3>}
      <ToolkitProvider
        keyField={!_.isEmpty(dataset) && dataset.length > 0 ? "uniqueId" : "_"}
        data={dataset}
        columns={customizeColumns(props.headers, props.dataset, props.isFilterEnabled)}
        columnToggle={columnToggle}
        search={search}
        exportCSV={{
          fileName: csvFilename,
        }}
      >
        {(toolkitProps: ToolkitProviderProps): JSX.Element => renderTable(toolkitProps, props, dataset)}
      </ToolkitProvider>
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
        {_.isEmpty(dataset) && _.isEmpty(props.headers) ? <div/> : renderToolKitProvider(props, dataset)}
      </div>
    </React.StrictMode>
  );
};

export { dataTableNext as DataTableNext };
