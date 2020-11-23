/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  --------
  We need className to override default styles from react-bootstrap and props
  spreading is the technique used by react-bootstrap-table2 creators to pass
  down props
  */
import BootstrapTable from "react-bootstrap-table-next";
import { Button } from "components/Button";
import { CustomToggleList } from "components/DataTableNext/customToggleList";
import { ExportCSVButtonWrapper } from "components/DataTableNext/exportCSVButton";
import type { ITableWrapperProps } from "components/DataTableNext/types";
import React from "react";
import { Search } from "react-bootstrap-table2-toolkit";
import { SizePerPageRenderer } from "components/DataTableNext/sizePerPageRenderer";
import { TooltipWrapper } from "components/TooltipWrapper";
import _ from "lodash";
import filterFactory from "react-bootstrap-table2-filter";
import paginationFactory from "react-bootstrap-table2-paginator";
import style from "components/DataTableNext/index.css";
import { useTranslation } from "react-i18next";
import {
  ButtonGroup,
  ButtonToolbar,
  Col,
  Glyphicon,
  Row,
} from "react-bootstrap";

export const TableWrapper: React.FC<ITableWrapperProps> = (
  // Readonly utility type doesn't seem to work on ITableWrapperProps
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<ITableWrapperProps>
): JSX.Element => {
  const { SearchBar } = Search;
  const { toolkitProps, tableProps, dataset } = props;
  const { columnToggleProps, searchProps, baseProps } = toolkitProps;
  const {
    bordered,
    defaultSorted,
    onUpdateEnableFilter,
    isFilterEnabled,
    pageSize,
    columnToggle = false,
    exportCsv,
    search,
    tableHeader,
    rowEvents,
    tableBody,
    selectionMode,
    striped,
  } = tableProps;
  const { t } = useTranslation();

  function handleUpdateEnableFilter(): void {
    if (!_.isUndefined(onUpdateEnableFilter)) {
      onUpdateEnableFilter();
    }
  }
  function handleNoData(): string {
    return t("dataTableNext.noDataIndication");
  }

  const isPaginationEnable: boolean =
    !_.isEmpty(dataset) && dataset.length > pageSize;

  const paginationOptions: PaginationProps = {
    sizePerPage: pageSize,
    sizePerPageRenderer: SizePerPageRenderer,
  };

  return (
    <div>
      <Row className={style.tableOptions}>
        <Col lg={9} md={8} sm={6} xs={12}>
          {(exportCsv || columnToggle || !_.isUndefined(isFilterEnabled)) && (
            <ButtonToolbar>
              {exportCsv && (
                <ButtonGroup>
                  <ExportCSVButtonWrapper {...toolkitProps} />
                </ButtonGroup>
              )}
              {columnToggle && (
                <ButtonGroup>
                  <CustomToggleList
                    propsTable={tableProps}
                    propsToggle={columnToggleProps}
                  />
                </ButtonGroup>
              )}
              {!_.isUndefined(isFilterEnabled) && (
                <ButtonGroup>
                  <TooltipWrapper message={t("dataTableNext.tooltip")}>
                    <Button onClick={handleUpdateEnableFilter}>
                      {isFilterEnabled ? (
                        <Glyphicon glyph={"minus"} />
                      ) : (
                        <Glyphicon glyph={"plus"} />
                      )}
                      &nbsp;
                      {t("dataTableNext.filters")}
                    </Button>
                  </TooltipWrapper>
                </ButtonGroup>
              )}
            </ButtonToolbar>
          )}
        </Col>
        {search && (
          <Col lg={3} md={4} sm={6} xs={12}>
            <SearchBar {...searchProps} className={style.searchBar} />
          </Col>
        )}
      </Row>
      <BootstrapTable
        {...baseProps}
        bordered={bordered}
        defaultSorted={
          _.isUndefined(defaultSorted) ? undefined : [defaultSorted]
        }
        filter={filterFactory()}
        headerClasses={
          _.isUndefined(tableHeader) ? style.tableHeader : tableHeader
        }
        hover={true}
        noDataIndication={handleNoData}
        pagination={
          isPaginationEnable ? paginationFactory(paginationOptions) : undefined
        }
        rowClasses={_.isUndefined(tableBody) ? style.tableBody : tableBody}
        rowEvents={rowEvents}
        selectRow={selectionMode}
        striped={striped}
        wrapperClasses={`table-responsive ${style.tableWrapper} ${
          bordered ? "" : style.borderNone
        }`}
      />
    </div>
  );
};
