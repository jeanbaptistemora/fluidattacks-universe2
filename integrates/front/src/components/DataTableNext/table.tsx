/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  --------
  We need className to override default styles from react-bootstrap and props
  spreading is the technique used by react-bootstrap-table2 creators to pass
  down props
  */
import {
  faEraser,
  faMinus,
  faSearchMinus,
  faSearchPlus,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { createRef, useEffect } from "react";
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
import type {
  ICustomSearchProps,
  IFilterProps,
  ITableWrapperProps,
} from "components/DataTableNext/types";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  ButtonGroup,
  ButtonToolbarRow,
  Filters,
  FlexAutoContainer,
  InputDateRange,
  InputNumber,
  InputRange,
  InputText,
  RangeContainer,
  SearchText,
  Select,
  SelectContainer,
  SelectDate,
  Small,
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
    bordered,
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
    onPageChange,
    search,
    rowEvents,
    selectionMode,
    striped,
  } = tableProps;
  const {
    customFiltersProps,
    hideResults,
    isCustomFilterEnabled,
    oneRowMessage = false,
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
    return t("dataTableNext.noDataIndication");
  }
  function handleClearFiltersButton(): void {
    if (!_.isUndefined(clearFiltersButton)) {
      clearFiltersButton();
    }
  }

  const enablePagination = dataset.length > pageSize;

  // eslint-disable-next-line @typescript-eslint/no-magic-numbers
  const listSizePerPage: number[] = [10, 20, 30, 50, 100, 200, 500, 1000];

  const paginationOptions: PaginationOptions = {
    onPageChange,
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

  const filterOption = (filter: IFilterProps): JSX.Element => {
    const {
      defaultValue,
      onChangeSelect,
      onChangeInput,
      rangeProps,
      selectOptions,
      placeholder = "",
      tooltipId,
      translateSelectOptions = true,
      type,
    } = filter;

    function handleChangeSelect(
      event: React.ChangeEvent<HTMLSelectElement>
    ): void {
      event.stopPropagation();
      if (onChangeSelect) {
        onChangeSelect(event);
      }
    }
    function handleChangeInput(
      event: React.ChangeEvent<HTMLInputElement>
    ): void {
      event.stopPropagation();
      if (onChangeInput) {
        onChangeInput(event);
      }
    }
    function handleChangeMax(event: React.ChangeEvent<HTMLInputElement>): void {
      event.stopPropagation();
      if (rangeProps?.onChangeMax) {
        rangeProps.onChangeMax(event);
      }
    }
    function handleChangeMin(event: React.ChangeEvent<HTMLInputElement>): void {
      event.stopPropagation();
      if (rangeProps?.onChangeMin) {
        rangeProps.onChangeMin(event);
      }
    }

    if (type === "date")
      return (
        <SelectDate
          onChange={handleChangeInput}
          style={
            defaultValue === ""
              ? {}
              : { boxShadow: "0 3px 5px #2e2e38", color: "#2e2e38" }
          }
          value={defaultValue}
        />
      );
    if (type === "select")
      return (
        <Select
          id={`select.${tooltipId}`}
          onChange={handleChangeSelect}
          style={
            defaultValue === ""
              ? {}
              : { boxShadow: "0 3px 5px #2e2e38", color: "#2e2e38" }
          }
          value={defaultValue === "" ? "__placeholder__" : defaultValue}
        >
          {defaultValue === "" ? (
            <option disabled={true} hidden={true} value={"__placeholder__"}>
              {t(placeholder)}
            </option>
          ) : (
            <option value={""}>{t("dataTableNext.allOptions")}</option>
          )}
          {Object.entries(selectOptions ?? {}).map(
            ([key, value]): JSX.Element => (
              <option key={value} value={key}>
                {translateSelectOptions
                  ? t(value.toString())
                  : value.toString()}
              </option>
            )
          )}
        </Select>
      );
    if (type === "number")
      return (
        <InputNumber
          min={0}
          onChange={handleChangeInput}
          placeholder={t(`${placeholder}`)}
          style={
            defaultValue === ""
              ? {}
              : { boxShadow: "0 3px 5px #2e2e38", color: "#2e2e38" }
          }
          type={"number"}
          value={defaultValue}
        />
      );
    if (type === "dateRange")
      return (
        <RangeContainer>
          <InputDateRange
            onChange={handleChangeMin}
            style={
              rangeProps?.defaultValue.min === ""
                ? { maxWidth: "11rem" }
                : {
                    boxShadow: "0 3px 5px #2e2e38",
                    color: "#2e2e38",
                    maxWidth: "11rem",
                  }
            }
            type={"date"}
            value={rangeProps?.defaultValue.min}
          />
          <div>
            <FontAwesomeIcon
              className={" h-100 mvh-auto mh2"}
              color={"gray"}
              icon={faMinus}
            />
          </div>
          <InputDateRange
            onChange={handleChangeMax}
            style={
              rangeProps?.defaultValue.max === ""
                ? { maxWidth: "11rem" }
                : {
                    boxShadow: "0 3px 5px #2e2e38",
                    color: "#2e2e38",
                    maxWidth: "11rem",
                  }
            }
            type={"date"}
            value={rangeProps?.defaultValue.max}
          />
        </RangeContainer>
      );
    if (type === "range")
      return (
        <RangeContainer>
          <InputRange
            onChange={handleChangeMin}
            placeholder={"Min"}
            step={rangeProps?.step}
            style={
              rangeProps?.defaultValue.min === ""
                ? {}
                : { boxShadow: "0 3px 5px #2e2e38", color: "#2e2e38" }
            }
            type={"number"}
            value={rangeProps?.defaultValue.min}
          />
          <div>
            <FontAwesomeIcon
              className={" h-100 mvh-auto"}
              color={"gray"}
              icon={faMinus}
            />
          </div>
          <InputRange
            onChange={handleChangeMax}
            placeholder={"Max"}
            step={rangeProps?.step}
            style={
              rangeProps?.defaultValue.max === ""
                ? {}
                : { boxShadow: "0 3px 5px #2e2e38", color: "#2e2e38" }
            }
            type={"number"}
            value={rangeProps?.defaultValue.max}
          />
        </RangeContainer>
      );

    return (
      <InputText
        onChange={handleChangeInput}
        placeholder={t(`${placeholder}`)}
        value={defaultValue}
      />
    );
  };

  const scrollbar: React.RefObject<HTMLDivElement> = createRef();
  const table: React.RefObject<HTMLDivElement> = createRef();
  const tableMimic: React.RefObject<HTMLDivElement> = createRef();

  function scrollTable(): void {
    if (table.current && scrollbar.current) {
      // eslint-disable-next-line fp/no-mutation
      table.current.children[0].scrollLeft = scrollbar.current.scrollLeft;
    }
  }

  function syncScrollbar(): void {
    const tableChild: HTMLElement | undefined = table.current?.children[0]
      ?.children[0] as HTMLElement;

    if (
      table.current &&
      tableMimic.current &&
      scrollbar.current &&
      !_.isUndefined(tableChild)
    ) {
      if (scrollbar.current.offsetWidth === tableChild.offsetWidth) {
        // eslint-disable-next-line fp/no-mutation
        scrollbar.current.style.visibility = "hidden";
      } else {
        // eslint-disable-next-line fp/no-mutation
        scrollbar.current.style.visibility = "visible";
      }

      // eslint-disable-next-line fp/no-mutation
      tableMimic.current.style.width = `${tableChild.offsetWidth}px`;
    }
  }

  useEffect(syncScrollbar, [
    scrollbar,
    scrollbar.current?.offsetWidth,
    table,
    tableMimic,
  ]);

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
                      onUpdate={syncScrollbar}
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
                          <FontAwesomeIcon icon={faSearchMinus} />
                        ) : (
                          <FontAwesomeIcon icon={faSearchPlus} />
                        )}
                        &nbsp;
                        {t("dataTableNext.filters")}
                      </Button>
                    </TooltipWrapper>
                  </ButtonGroup>
                )}
                <ButtonGroup>{extraButtons}</ButtonGroup>
                {!_.isUndefined(isCustomFilterEnabled) && (
                  <ButtonGroup>
                    <TooltipWrapper
                      id={"CustomFilterTooltip"}
                      message={t("dataTableNext.tooltip")}
                    >
                      <Button
                        id={"filter-config"}
                        onClick={handleUpdateEnableCustomFilter}
                      >
                        {isCustomFilterEnabled ? (
                          <FontAwesomeIcon icon={faSearchMinus} />
                        ) : (
                          <FontAwesomeIcon icon={faSearchPlus} />
                        )}
                        &nbsp;
                        {t("dataTableNext.filters")}
                      </Button>
                    </TooltipWrapper>
                  </ButtonGroup>
                )}
                {resultSize && oneRowMessage && (
                  <ButtonGroup>
                    <div className={"flex items-end justify-end ma0 ml2 pa0"}>
                      {`${t("dataTableNext.filterRes1")}: ${
                        resultSize.current
                      } ${t("dataTableNext.filterRes2")} ${resultSize.total}`}
                    </div>
                  </ButtonGroup>
                )}
                {!_.isUndefined(isCustomSearchEnabled) &&
                  isCustomSearchEnabled &&
                  searchPosition === "left" && (
                    <ButtonGroup>
                      <div className={"pb1 ph1-5 w-100"}>
                        <SearchText
                          onChange={onUpdateCustomSearch}
                          placeholder={t("dataTableNext.search")}
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
                          placeholder={t("dataTableNext.search")}
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
          {!_.isUndefined(isCustomFilterEnabled) && isCustomFilterEnabled && (
            <Filters>
              {customFiltersProps?.map(
                (filter: IFilterProps): JSX.Element | undefined => {
                  const {
                    tooltipId,
                    tooltipMessage,
                    placeholder = "",
                  } = filter;

                  return _.isUndefined(filter.omit) || !filter.omit ? (
                    <SelectContainer key={`container.${filter.tooltipId}`}>
                      <TooltipWrapper
                        id={tooltipId}
                        message={t(tooltipMessage)}
                        placement={"top"}
                      >
                        {filterOption(filter)}
                      </TooltipWrapper>
                      {filter.type === "dateRange" ||
                      filter.type === "range" ? (
                        <Small>{t(placeholder)}</Small>
                      ) : undefined}
                    </SelectContainer>
                  ) : undefined;
                }
              )}
              <SelectContainer />

              <FlexAutoContainer>
                <Button
                  className={"lh-copy fr"}
                  onClick={handleClearFiltersButton}
                >
                  <FontAwesomeIcon icon={faEraser} />
                  &nbsp;
                  {t("dataTableNext.clearFilters")}
                </Button>
              </FlexAutoContainer>
            </Filters>
          )}
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
        <p>{`${t("dataTableNext.results", {
          matches: resultSize.current,
          total: resultSize.total,
        })}`}</p>
      )}
      {resultSize && !oneRowMessage && (
        <div className={"fw4 mb0 nt1"}>
          {`${t("dataTableNext.filterRes1")}: ${resultSize.current} ${t(
            "dataTableNext.filterRes2"
          )} ${resultSize.total}`}
        </div>
      )}
      <div ref={table}>
        <BootstrapTable
          {...baseProps}
          bootstrap4={true}
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
          headerClasses={style.tableHeader}
          hover={true}
          noDataIndication={handleNoData}
          pagination={
            enablePagination ? paginationFactory(paginationOptions) : undefined
          }
          rowClasses={style.tableBody}
          rowEvents={rowEvents}
          selectRow={selectionMode as SelectRowProps<unknown>}
          striped={striped}
          wrapperClasses={`f6 mw-100 overflow-hidden ${style.tableWrapper}`}
        />
      </div>
      <div
        className={`overflow-x-scroll overflow-y-hidden ${style.scrollbar}`}
        onScroll={scrollTable}
        ref={scrollbar}
      >
        <div className={style.tableMimic} ref={tableMimic} />
      </div>
    </div>
  );
};
