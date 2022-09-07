/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  --------
  We need className to override default styles from react-bootstrap and props
  spreading is the technique used by react-bootstrap-table2 creators to pass
  down props
  */
import { faSearchMinus, faSearchPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import type { FC } from "react";
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

import { CustomToggleList } from "./customToggleList";
import { renderExpandIcon, renderHeaderExpandIcon } from "./expandIcon";
import { ExportCSVButtonWrapper } from "./exportCSVButton";
import { Filters } from "./Filters";
import style from "./index.css";
import { PageListRenderer } from "./PageListRenderer";
import { PaginationTotalRenderer } from "./PaginationTotalRenderer";
import { SizePerPageRenderer } from "./SizePerPageRenderer";
import { TableContainer } from "./styles";
import type { ITableWrapperProps } from "./types";

import { Button } from "components/Button";
import { Gap } from "components/Layout";
import { Tooltip } from "components/Tooltip";
import {
  ButtonToolbarRow,
  SearchText,
  TableOptionsColBar,
} from "styles/styledComponents";

// eslint-disable-next-line complexity
const TableWrapper: FC<ITableWrapperProps> = ({
  dataset,
  onSizePerPageChange,
  preferredPageSize,
  toolkitProps,
  tableProps,
}: Readonly<ITableWrapperProps>): JSX.Element => {
  const { SearchBar } = Search;
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
    hideResults = false,
    isCustomFilterEnabled,
    onUpdateEnableCustomFilter,
    resultSize,
  } = customFilters ?? {};
  const {
    customSearchDefault,
    isCustomSearchEnabled,
    onUpdateCustomSearch,
    position: searchPosition = "left",
  } = customSearch ?? {};
  const { t } = useTranslation();

  function handleUpdateEnableFilter(): void {
    onUpdateEnableFilter?.();
  }
  function handleUpdateEnableCustomFilter(): void {
    onUpdateEnableCustomFilter?.();
  }

  function handleNoData(): string {
    return t("table.noDataIndication");
  }

  const enablePagination = dataset.length > pageSize;

  // eslint-disable-next-line @typescript-eslint/no-magic-numbers
  const listSizePerPage: number[] = [
    10,
    20,
    50,
    100,
    200,
    500,
    Math.min(1000, dataset.length),
  ];

  const paginationOptions: PaginationOptions = {
    onSizePerPageChange,
    pageListRenderer: PageListRenderer,
    paginationSize: 10,
    paginationTotalRenderer: PaginationTotalRenderer,
    showTotal: true,
    sizePerPage: preferredPageSize,
    sizePerPageList: listSizePerPage.filter(
      (el): boolean => el <= dataset.length
    ),
    sizePerPageRenderer: SizePerPageRenderer,
  };

  return (
    <div>
      <div className={"flex flex-wrap mb2"}>
        <div className={"w-100"}>
          {exportCsv ||
          columnToggle ||
          !_.isUndefined(isFilterEnabled) ||
          !_.isUndefined(isCustomFilterEnabled) ||
          !_.isUndefined(customSearchDefault) ||
          extraButtons !== undefined ||
          extraButtonsRight !== undefined ? (
            <div className={`flex flex-wrap justify-between pa0 w-100`}>
              <Gap>
                {extraButtons}
                {exportCsv && <ExportCSVButtonWrapper {...toolkitProps} />}
                {columnToggle && (
                  <CustomToggleList
                    propsTable={tableProps}
                    propsToggle={columnToggleProps}
                  />
                )}
                {!_.isUndefined(isFilterEnabled) && (
                  <Tooltip id={"filterTooltip"} tip={t("table.tooltip")}>
                    <Button
                      onClick={handleUpdateEnableFilter}
                      variant={"secondary"}
                    >
                      <FontAwesomeIcon
                        icon={isFilterEnabled ? faSearchMinus : faSearchPlus}
                      />
                      &nbsp;
                      {t("table.filters")}
                    </Button>
                  </Tooltip>
                )}
                {!_.isUndefined(isCustomFilterEnabled) && (
                  <Tooltip id={"CustomFilterTooltip"} tip={t("table.tooltip")}>
                    <Button
                      id={"filter-config"}
                      onClick={handleUpdateEnableCustomFilter}
                    >
                      <FontAwesomeIcon
                        icon={
                          isCustomFilterEnabled ? faSearchMinus : faSearchPlus
                        }
                      />
                      &nbsp;
                      {t("table.filters")}
                    </Button>
                  </Tooltip>
                )}
                {!_.isUndefined(isCustomSearchEnabled) &&
                  isCustomSearchEnabled &&
                  searchPosition === "left" && (
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
                  )}
              </Gap>
              {extraButtonsRight === undefined &&
              isCustomSearchEnabled === false ? undefined : (
                <div className={"dib"}>
                  {searchPosition === "right" ? (
                    <div className={"nt1-l nt0 pb1 pl2 pt1 pt0-m pt0-l w-100"}>
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
                  ) : undefined}
                  {extraButtonsRight}
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
      {resultSize && !hideResults ? (
        <Tooltip id={"tableResultTooltip"} tip={t("table.results.tooltip")}>
          <p>
            {t("table.results.text", {
              matches: resultSize.current,
              total: resultSize.total,
            })}
          </p>
        </Tooltip>
      ) : undefined}
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

export { TableWrapper };
