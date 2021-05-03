/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  --------
  We need className to override default styles from react-bootstrap and props
  spreading is the technique used by react-bootstrap-table2 creators to pass
  down props
  */
import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React from "react";
import BootstrapTable from "react-bootstrap-table-next";
import filterFactory from "react-bootstrap-table2-filter";
import paginationFactory from "react-bootstrap-table2-paginator";
import { Search } from "react-bootstrap-table2-toolkit";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { CustomToggleList } from "components/DataTableNext/customToggleList";
import { ExportCSVButtonWrapper } from "components/DataTableNext/exportCSVButton";
import style from "components/DataTableNext/index.css";
import { SizePerPageRenderer } from "components/DataTableNext/sizePerPageRenderer";
import type { ITableWrapperProps } from "components/DataTableNext/types";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  ButtonGroup,
  ButtonToolbarLeft,
  ButtonToolbarRow,
  TableOptionsColBar,
  TableOptionsColBtn,
} from "styles/styledComponents";

export const TableWrapper: React.FC<ITableWrapperProps> = (
  // Readonly utility type doesn't seem to work on ITableWrapperProps
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<ITableWrapperProps>
): JSX.Element => {
  const { SearchBar } = Search;
  const { toolkitProps, tableProps, dataset, extraButtons } = props;
  const { columnToggleProps, searchProps, baseProps } = toolkitProps;
  const defaultPages: number = 5;
  const defaultInitPages: number = 1;
  const {
    bordered,
    defaultSorted,
    onUpdateEnableFilter,
    isFilterEnabled,
    numPages = defaultPages,
    pageSize,
    onSizePerPageChange,
    columnToggle = false,
    exportCsv,
    onPageChange,
    search,
    tableHeader,
    tableSize = "",
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
    numPages === defaultInitPages ||
    (!_.isEmpty(dataset) && dataset.length > pageSize);

  const paginationOptions: PaginationProps = {
    onPageChange,
    onSizePerPageChange,
    paginationSize: numPages,
    sizePerPage: pageSize,
    sizePerPageRenderer: SizePerPageRenderer,
  };

  return (
    <div>
      <div className={style.tableOptions}>
        <TableOptionsColBtn>
          <div>
            <ButtonToolbarLeft>
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
                  <TooltipWrapper
                    id={"filterTooltip"}
                    message={t("dataTableNext.tooltip")}
                  >
                    <Button onClick={handleUpdateEnableFilter}>
                      {isFilterEnabled ? (
                        <FontAwesomeIcon icon={faMinus} />
                      ) : (
                        <FontAwesomeIcon icon={faPlus} />
                      )}
                      &nbsp;
                      {t("dataTableNext.filters")}
                    </Button>
                  </TooltipWrapper>
                </ButtonGroup>
              )}
              <ButtonGroup>{extraButtons}</ButtonGroup>
            </ButtonToolbarLeft>
          </div>
        </TableOptionsColBtn>
        {search && (
          <TableOptionsColBar>
            <ButtonToolbarRow>
              <SearchBar {...searchProps} className={style.searchBar} />
            </ButtonToolbarRow>
          </TableOptionsColBar>
        )}
      </div>
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
        wrapperClasses={`table-responsive mw-100 overflow-x-auto ${tableSize}
          ${style.tableWrapper} ${bordered ? "" : style.borderNone}`}
      />
    </div>
  );
};
