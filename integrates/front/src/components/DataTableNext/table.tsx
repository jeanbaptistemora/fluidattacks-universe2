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
import type {
  IFilterProps,
  ITableWrapperProps,
} from "components/DataTableNext/types";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  ButtonGroup,
  ButtonToolbarLeft,
  ButtonToolbarRow,
  Filters,
  InputNumber,
  InputText,
  SearchContainer,
  SearchText,
  Select,
  SelectContainer,
  SelectDate,
  Small,
  TableOptionsColBar,
  TableOptionsColBtn,
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
    customFilters,
    customSearch,
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
    rowEvents,
    selectionMode,
    striped,
  } = tableProps;
  const {
    customFiltersProps,
    isCustomFilterEnabled,
    onUpdateEnableCustomFilter,
  } = customFilters ?? {};
  const { customSearchDefault, isCustomSearchEnabled, onUpdateCustomSearch } =
    customSearch ?? {};
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

  const filterOption = (filter: IFilterProps): JSX.Element => {
    const {
      defaultValue,
      onChangeSelect,
      onChangeInput,
      selectOptions,
      placeholder = "",
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

    if (type === "date")
      return (
        <SelectDate defaultValue={defaultValue} onChange={handleChangeInput} />
      );
    if (type === "select")
      return (
        <Select
          defaultValue={defaultValue === "" ? "__placeholder__" : defaultValue}
          onChange={handleChangeSelect}
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
                {t(value.toString())}
              </option>
            )
          )}
        </Select>
      );
    if (type === "number")
      return (
        <InputNumber
          defaultValue={defaultValue}
          min={0}
          onChange={handleChangeInput}
          placeholder={t(`${placeholder}`)}
          type={"number"}
        />
      );

    return (
      <InputText
        defaultValue={defaultValue}
        onChange={handleChangeInput}
        placeholder={t(`${placeholder}`)}
      />
    );
  };

  return (
    <div>
      <div className={`flex flex-wrap ${style.tableOptions}`}>
        <div>
          {exportCsv ||
          columnToggle ||
          !_.isUndefined(isFilterEnabled) ||
          !_.isUndefined(isCustomFilterEnabled) ||
          !_.isUndefined(customSearchDefault) ||
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
                {!_.isUndefined(isCustomFilterEnabled) && (
                  <ButtonGroup>
                    <TooltipWrapper
                      id={"CustomFilterTooltip"}
                      message={t("dataTableNext.tooltip")}
                    >
                      <Button onClick={handleUpdateEnableCustomFilter}>
                        {isCustomFilterEnabled ? (
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
                {!_.isUndefined(isCustomSearchEnabled) &&
                  isCustomSearchEnabled && (
                    <ButtonGroup>
                      <SearchContainer>
                        <SearchText
                          defaultValue={customSearchDefault ?? ""}
                          onChange={onUpdateCustomSearch}
                          placeholder={t("dataTableNext.search")}
                        />
                      </SearchContainer>
                    </ButtonGroup>
                  )}
              </ButtonToolbarLeft>
            </TableOptionsColBtn>
          ) : undefined}
          {!_.isUndefined(isCustomFilterEnabled) && isCustomFilterEnabled && (
            <Filters>
              {customFiltersProps?.map((filter: IFilterProps): JSX.Element => {
                const { tooltipId, tooltipMessage, placeholder = "" } = filter;

                return (
                  <SelectContainer key={`container.${filter.tooltipId}`}>
                    <TooltipWrapper
                      id={tooltipId}
                      message={t(tooltipMessage)}
                      placement={"top"}
                    >
                      {filterOption(filter)}
                    </TooltipWrapper>
                    <Small>{t(placeholder)}</Small>
                  </SelectContainer>
                );
              })}
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
        wrapperClasses={`mw-100 overflow-x-auto
          ${style.tableWrapper} ${bordered ? "" : style.borderNone}`}
      />
    </div>
  );
};
