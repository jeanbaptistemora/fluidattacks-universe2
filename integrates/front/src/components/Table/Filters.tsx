/* eslint-disable react/forbid-component-props */
import { faEraser, faMinus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import type { ICustomFiltersProps, IFilterProps, ITableProps } from "./types";

import { Button } from "components/Button";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  Filters as FiltersContainer,
  FlexAutoContainer,
  InputDateRange,
  InputNumber,
  InputRange,
  InputText,
  RangeContainer,
  Select,
  SelectContainer,
  SelectDate,
  Small,
} from "styles/styledComponents";
import { translate } from "utils/translations/translate";

const filterOption = ({
  defaultValue,
  onChangeSelect,
  onChangeInput,
  rangeProps,
  selectOptions,
  placeholder = "",
  tooltipId,
  translateSelectOptions = true,
  type,
}: IFilterProps): JSX.Element => {
  function handleChangeSelect(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    event.stopPropagation();
    if (onChangeSelect) {
      onChangeSelect(event);
    }
  }
  function handleChangeInput(event: React.ChangeEvent<HTMLInputElement>): void {
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

  if (type === "date") {
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
  }

  if (type === "select") {
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
            {translate.t(placeholder)}
          </option>
        ) : (
          <option value={""}>{translate.t("table.allOptions")}</option>
        )}
        {Object.entries(selectOptions ?? {}).map(
          ([key, value]): JSX.Element => (
            <option key={value} value={key}>
              {translateSelectOptions
                ? translate.t(value.toString())
                : value.toString()}
            </option>
          )
        )}
      </Select>
    );
  }

  if (type === "number") {
    return (
      <InputNumber
        min={0}
        onChange={handleChangeInput}
        placeholder={translate.t(`${placeholder}`)}
        style={
          defaultValue === ""
            ? {}
            : { boxShadow: "0 3px 5px #2e2e38", color: "#2e2e38" }
        }
        type={"number"}
        value={defaultValue}
      />
    );
  }
  if (type === "dateRange") {
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
          <FontAwesomeIcon color={"gray"} icon={faMinus} />
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
  }
  if (type === "range") {
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
          <FontAwesomeIcon color={"gray"} icon={faMinus} />
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
  }

  return (
    <InputText
      onChange={handleChangeInput}
      placeholder={translate.t(`${placeholder}`)}
      value={defaultValue}
    />
  );
};

const Filters = ({
  clearFiltersButton,
  customFiltersProps,
}: Pick<ICustomFiltersProps, "customFiltersProps"> &
  Pick<ITableProps, "clearFiltersButton">): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FiltersContainer>
      {customFiltersProps.map(
        (filter: IFilterProps): JSX.Element | undefined => {
          const isRange =
            filter.type === "dateRange" || filter.type === "range";

          return filter.omit === true ? undefined : (
            <SelectContainer key={filter.tooltipId}>
              <TooltipWrapper
                id={filter.tooltipId}
                message={t(filter.tooltipMessage)}
                placement={"top"}
              >
                {filterOption(filter)}
              </TooltipWrapper>
              {isRange ? (
                <Small>{t(filter.placeholder ?? "")}</Small>
              ) : undefined}
            </SelectContainer>
          );
        }
      )}
      <FlexAutoContainer>
        <Button
          className={"lh-copy fr"}
          onClick={clearFiltersButton}
          variant={"secondary"}
        >
          <FontAwesomeIcon icon={faEraser} />
          &nbsp;{t("table.clearFilters")}
        </Button>
      </FlexAutoContainer>
    </FiltersContainer>
  );
};

export { Filters };
