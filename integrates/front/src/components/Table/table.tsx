/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  --------
  We need className to override default styles from react-bootstrap and props
  spreading is the technique used by react-bootstrap-table2 creators to pass
  down props
  */
import { faSearchMinus, faSearchPlus } from "@fortawesome/free-solid-svg-icons";
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
import { Filters } from "./Filters";
import { TableContainer } from "./styles";

import { Button } from "components/Button";
import { CustomToggleList } from "components/Table/customToggleList";
import { ExportCSVButtonWrapper } from "components/Table/exportCSVButton";
import style from "components/Table/index.css";
import { SizePerPageRenderer } from "components/Table/sizePerPageRenderer";
import type {
  ICustomSearchProps,
  ITableWrapperProps,
} from "components/Table/types";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  ButtonGroup,
  ButtonToolbarRow,
  SearchText,
  TableOptionsColBar,
} from "styles/styledComponents";

// eslint-disable-next-line complexity
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
    clearFiltersButton,
    customFilters,
    customSearch,
    defaultSorted,
    expandRow,
    extraButtons,
    extraButtonsRight,
    onUpdateEnableFilter,
    isFilterEnabled,
    pageSize,
    columnToggle = false,
    exportCsv,
    search,
    rowEvents,
    rowSize,
    selectionMode,
  } = tableProps;
  const {
    customFiltersProps,
    hideResults,
    isCustomFilterEnabled,
    onUpdateEnableCustomFilter,
    resultSize,
  } = customFilters ?? {};
  const {
    customSearchDefault,
    isCustomSearchEnabled,
    onUpdateCustomSearch,
    position,
  } = customSearch ?? {};
  const searchPosition: ICustomSearchProps["position"] =
    position === undefined || position === "left" ? "left" : "right";
  const shoulShowResults: boolean = hideResults === undefined || !hideResults;
  const { t } = useTranslation();

  function handleUpdateEnableFilter(): void {
    if (!_.isUndefined(onUpdateEnableFilter)) {
      onUpdateEnableFilter();
    }
  }
  function handleUpdateEnableCustomFilter(): void {
    if (!_.isUndefined(onUpdateEnableCustomFilter)) {
      onUpdateEnableCustomFilter();
    }
  }

  function handleNoData(): string {
    return t("table.noDataIndication");
  }

  const enablePagination = dataset.length > pageSize;

  // eslint-disable-next-line @typescript-eslint/no-magic-numbers
  const listSizePerPage: number[] = [10, 20, 30, 50, 100, 200, 500, 1000];

  const paginationOptions: PaginationOptions = {
    onSizePerPageChange,
    paginationSize: 10,
    sizePerPage: preferredPageSize,
    sizePerPageList: listSizePerPage.slice(
      0,
      listSizePerPage.findIndex(
        (element): boolean => element >= dataset.length
      ) + 1
    ),
    sizePerPageRenderer:
      SizePerPageRenderer as unknown as PaginationOptions["sizePerPageRenderer"],
  };

  return (
    <div>
      <div className={`flex flex-wrap ${style.tableOptions}`}>
        <div className={"w-100"}>
          {exportCsv ||
          columnToggle ||
          !_.isUndefined(isFilterEnabled) ||
          !_.isUndefined(isCustomFilterEnabled) ||
          !_.isUndefined(customSearchDefault) ||
          extraButtons !== undefined ||
          extraButtonsRight !== undefined ? (
            <div
              className={`flex flex-wrap justify-between pa0 table-btn w-100`}
            >
              <div>
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
                      message={t("table.tooltip")}
                    >
                      <Button
                        onClick={handleUpdateEnableFilter}
                        variant={"secondary"}
                      >
                        {isFilterEnabled ? (
                          <FontAwesomeIcon icon={faSearchMinus} />
                        ) : (
                          <FontAwesomeIcon icon={faSearchPlus} />
                        )}
                        &nbsp;
                        {t("table.filters")}
                      </Button>
                    </TooltipWrapper>
                  </ButtonGroup>
                )}
                <ButtonGroup>{extraButtons}</ButtonGroup>
                {!_.isUndefined(isCustomFilterEnabled) && (
                  <ButtonGroup>
                    <TooltipWrapper
                      id={"CustomFilterTooltip"}
                      message={t("table.tooltip")}
                    >
                      <Button
                        id={"filter-config"}
                        onClick={handleUpdateEnableCustomFilter}
                        variant={"secondary"}
                      >
                        {isCustomFilterEnabled ? (
                          <FontAwesomeIcon icon={faSearchMinus} />
                        ) : (
                          <FontAwesomeIcon icon={faSearchPlus} />
                        )}
                        &nbsp;
                        {t("table.filters")}
                      </Button>
                    </TooltipWrapper>
                  </ButtonGroup>
                )}
                {!_.isUndefined(isCustomSearchEnabled) &&
                  isCustomSearchEnabled &&
                  searchPosition === "left" && (
                    <ButtonGroup>
                      <div className={"pb1 ph1-5 w-100"}>
                        <SearchText
                          onChange={onUpdateCustomSearch}
                          placeholder={t("table.search")}
                          style={
                            customSearchDefault === ""
                              ? {}
                              : {
                                  boxShadow: "0 3px 5px #2e2e38",
                                  color: "#2e2e38",
                                }
                          }
                          value={customSearchDefault ?? ""}
                        />
                      </div>
                    </ButtonGroup>
                  )}
              </div>
              {extraButtonsRight === undefined &&
              isCustomSearchEnabled === false ? undefined : (
                <div>
                  {searchPosition === "right" ? (
                    <ButtonGroup>
                      <div
                        className={"nt1-l nt0 pb1 pl2 pt1 pt0-m pt0-l w-100"}
                      >
                        <SearchText
                          defaultValue={customSearchDefault ?? ""}
                          onChange={onUpdateCustomSearch}
                          placeholder={t("table.search")}
                          style={
                            customSearchDefault === ""
                              ? {}
                              : {
                                  boxShadow: "0 3px 5px #2e2e38",
                                  color: "#2e2e38",
                                }
                          }
                          value={customSearchDefault ?? ""}
                        />
                      </div>
                    </ButtonGroup>
                  ) : undefined}
                  <ButtonGroup>{extraButtonsRight}</ButtonGroup>
                </div>
              )}
            </div>
          ) : undefined}
          {isCustomFilterEnabled === true && customFiltersProps ? (
            <Filters
              clearFiltersButton={clearFiltersButton}
              customFiltersProps={customFiltersProps}
            />
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
      {resultSize && shoulShowResults && (
        <p>
          {t("table.results", {
            matches: resultSize.current,
            total: resultSize.total,
          })}
        </p>
      )}
      <TableContainer
        isRowFunctional={rowEvents !== undefined}
        rowSize={rowSize ?? "bold"}
      >
        <BootstrapTable
          {...baseProps}
          bootstrap4={true}
          bordered={false}
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
          hover={false}
          noDataIndication={handleNoData}
          pagination={
            enablePagination ? paginationFactory(paginationOptions) : undefined
          }
          rowEvents={rowEvents}
          selectRow={selectionMode as SelectRowProps<unknown>}
        />
      </TableContainer>
    </div>
  );
};
