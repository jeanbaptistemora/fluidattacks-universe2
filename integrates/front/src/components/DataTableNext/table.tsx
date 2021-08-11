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
import type {
  PaginationOptions,
  SelectRowProps,
} from "react-bootstrap-table-next";
import BootstrapTable from "react-bootstrap-table-next";
import filterFactory from "react-bootstrap-table2-filter";
import paginationFactory from "react-bootstrap-table2-paginator";
import { Search } from "react-bootstrap-table2-toolkit";
import { useTranslation } from "react-i18next";

import { renderExpandIcon, renderHeaderExpandIcon } from "./expandIcon";

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
  props: Readonly<ITableWrapperProps>
): JSX.Element => {
  const { SearchBar } = Search;
  const {
    dataset,
    onSizePerPageChange,
    preferredPageSize,
    toolkitProps,
    tableProps,
  } = props;
  const { columnToggleProps, searchProps, baseProps } = toolkitProps;
  const {
    bordered,
    defaultSorted,
    expandRow,
    extraButtons,
    onUpdateEnableFilter,
    isFilterEnabled,
    pageSize,
    columnToggle = false,
    exportCsv,
    onPageChange,
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

  const enablePagination = dataset.length > pageSize;

  const paginationOptions: PaginationOptions = {
    onPageChange,
    onSizePerPageChange,
    sizePerPage: preferredPageSize,
    // eslint-disable-next-line @typescript-eslint/no-magic-numbers
    sizePerPageList: [10, 25, 30, 50, 100, 200, 500, 1000],
    sizePerPageRenderer:
      SizePerPageRenderer as unknown as PaginationOptions["sizePerPageRenderer"],
  };

  return (
    <div>
      <div className={`flex flex-wrap ${style.tableOptions}`}>
        <div className={"w-80"}>
          {exportCsv ||
          columnToggle ||
          !_.isUndefined(isFilterEnabled) ||
          extraButtons !== undefined ? (
            <TableOptionsColBtn>
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
            </TableOptionsColBtn>
          ) : undefined}
        </div>
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
        expandRow={
          expandRow === undefined
            ? undefined
            : {
                expandColumnRenderer: renderExpandIcon,
                expandHeaderColumnRenderer: renderHeaderExpandIcon,
                ...expandRow,
              }
        }
        filter={filterFactory()}
        headerClasses={
          _.isUndefined(tableHeader) ? style.tableHeader : tableHeader
        }
        hover={true}
        noDataIndication={handleNoData}
        pagination={
          enablePagination ? paginationFactory(paginationOptions) : undefined
        }
        rowClasses={_.isUndefined(tableBody) ? style.tableBody : tableBody}
        rowEvents={rowEvents}
        selectRow={selectionMode as SelectRowProps<unknown>}
        striped={striped}
        wrapperClasses={`mw-100 overflow-x-auto
          ${style.tableWrapper} ${bordered ? "" : style.borderNone}`}
      />
    </div>
  );
};
