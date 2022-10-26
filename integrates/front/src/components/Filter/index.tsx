/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";
import React from "react";
import type { Dispatch, SetStateAction } from "react";

import {
  FormikDate,
  FormikInput,
  FormikNumber,
  FormikSelect,
} from "components/Input/Formik";
import { Col, Row } from "components/Layout";

interface IFilter<IData extends object> {
  filterFn?:
    | "caseInsensitive"
    | "caseSensitive"
    | "includesInArray"
    | "includesInsensitive"
    | "includesSensitive";
  id: string;
  key: keyof IData | ((arg0: object) => boolean);
  label?: string;
  rangeValues?: [string, string];
  selectOptions?: string[];
  type: "dateRange" | "number" | "numberRange" | "select" | "text";
  value?: string;
}

interface IFiltersProps<IData extends object> {
  filters: IFilter<IData>[];
  setFilters: Dispatch<SetStateAction<IFilter<IData>[]>>;
}

const useFilters = <IData extends object>(
  data: IData[],
  filters: IFilter<IData>[]
): IData[] => {
  function handleTextSelectCases(
    dataPoint: IData,
    filter: IFilter<IData>
  ): boolean {
    if (typeof filter.key === "function") return filter.key(dataPoint);
    if (filter.value === "" || filter.value === undefined) return true;

    switch (filter.filterFn) {
      case "caseSensitive":
        return String(dataPoint[filter.key]) === filter.value;

      case "includesSensitive":
        return String(dataPoint[filter.key]).includes(filter.value);

      case "includesInsensitive":
        return String(dataPoint[filter.key])
          .toLowerCase()
          .includes(filter.value.toLowerCase());

      case "includesInArray": {
        const array: unknown[] = JSON.parse(String(dataPoint[filter.key]));

        return array.includes(filter.value);
      }

      case "caseInsensitive":
      default:
        return (
          String(dataPoint[filter.key]).toLowerCase() ===
          filter.value.toLowerCase()
        );
    }
  }

  function handleNumberCase(dataPoint: IData, filter: IFilter<IData>): boolean {
    if (typeof filter.key === "function") return filter.key(dataPoint);

    return _.isEmpty(filter.value)
      ? true
      : String(dataPoint[filter.key]) === filter.value;
  }

  function checkAllFilters(dataPoint: IData): boolean {
    return filters.every((filter): boolean => {
      if (typeof filter.key === "function") return filter.key(dataPoint);
      switch (filter.type) {
        case "text":
        case "select":
          return handleTextSelectCases(dataPoint, filter);

        case "number":
          return handleNumberCase(dataPoint, filter);

        case "numberRange": {
          if (filter.rangeValues === undefined) return true;
          const isLower = _.isEmpty(filter.rangeValues[0])
            ? true
            : parseInt(String(dataPoint[filter.key]), 10) <=
              parseInt(filter.rangeValues[0], 10);

          const isHigher = _.isEmpty(filter.rangeValues[1])
            ? true
            : parseInt(String(dataPoint[filter.key]), 10) >=
              parseInt(filter.rangeValues[1], 10);

          return isLower && isHigher;
        }

        default:
          return true;
      }
    });
  }

  return data.filter((entry: IData): boolean => checkAllFilters(entry));
};

const Filters = <IData extends object>({
  filters,
  setFilters,
}: IFiltersProps<IData>): JSX.Element => {
  function onValueChangeHandler(
    id: string
  ): (event: React.ChangeEvent<HTMLInputElement>) => void {
    return (event: React.ChangeEvent<HTMLInputElement>): void => {
      setFilters(
        filters.map((filter): IFilter<IData> => {
          if (filter.id === id) {
            return {
              ...filter,
              value: event.target.value,
            };
          }

          return filter;
        })
      );
    };
  }

  return (
    <React.Fragment>
      {filters.map((filter: IFilter<IData>): JSX.Element => {
        switch (filter.type) {
          case "text": {
            return (
              <FormikInput
                field={{
                  name: filter.id,
                  onBlur: (): void => undefined,
                  onChange: onValueChangeHandler(filter.id),
                  value: filter.value ?? "",
                }}
                form={{ errors: {}, touched: {} }}
                label={filter.label}
                name={filter.id}
              />
            );
          }
          case "number": {
            return (
              <FormikNumber
                field={{
                  name: filter.id,
                  onBlur: (): void => undefined,
                  onChange: onValueChangeHandler(filter.id),
                  value: filter.value === undefined ? "" : String(filter.value),
                }}
                form={{ errors: {}, touched: {} }}
                label={filter.label}
                name={filter.id}
              />
            );
          }
          case "numberRange": {
            return (
              <Row>
                <Col lg={50} md={50}>
                  <FormikNumber
                    field={{
                      name: filter.id,
                      onBlur: (): void => undefined,
                      onChange: onValueChangeHandler(filter.id),
                      value:
                        filter.rangeValues?.[0] === undefined
                          ? ""
                          : String(filter.rangeValues[0]),
                    }}
                    form={{ errors: {}, touched: {} }}
                    label={filter.label}
                    name={filter.id}
                    placeholder={"Min"}
                  />
                </Col>
                <Col lg={50} md={50}>
                  <FormikNumber
                    field={{
                      name: filter.id,
                      onBlur: (): void => undefined,
                      onChange: onValueChangeHandler(filter.id),
                      value:
                        filter.rangeValues?.[1] === undefined
                          ? ""
                          : String(filter.rangeValues[1]),
                    }}
                    form={{ errors: {}, touched: {} }}
                    label={""}
                    name={filter.id}
                    placeholder={"Max"}
                  />
                </Col>
              </Row>
            );
          }
          case "select": {
            return (
              <FormikSelect
                field={{
                  name: filter.id,
                  onBlur: (): void => undefined,
                  onChange: onValueChangeHandler(filter.id),
                  value: filter.value ?? "",
                }}
                form={{ errors: {}, touched: {} }}
                label={filter.label}
                name={filter.id}
              >
                <option value={""}>{"All"}</option>
                {filter.selectOptions?.map(
                  (value): JSX.Element => (
                    <option key={value} value={value}>
                      {value}
                    </option>
                  )
                )}
              </FormikSelect>
            );
          }
          case "dateRange": {
            return (
              <Row>
                <Col lg={50} md={50}>
                  <FormikDate
                    field={{
                      name: filter.id,
                      onBlur: (): void => undefined,
                      onChange: onValueChangeHandler(filter.id),
                      value:
                        filter.rangeValues?.[0] === undefined
                          ? ""
                          : new Date(filter.rangeValues[0])
                              .toISOString()
                              .split("T")[0],
                    }}
                    form={{ errors: {}, touched: {} }}
                    label={filter.label}
                    name={filter.id}
                  />
                </Col>
                <Col lg={50} md={50}>
                  <FormikDate
                    field={{
                      name: filter.id,
                      onBlur: (): void => undefined,
                      onChange: onValueChangeHandler(filter.id),
                      value:
                        filter.rangeValues?.[1] === undefined
                          ? ""
                          : new Date(filter.rangeValues[1])
                              .toISOString()
                              .split("T")[0],
                    }}
                    form={{ errors: {}, touched: {} }}
                    label={""}
                    name={filter.id}
                  />
                </Col>
              </Row>
            );
          }
          default: {
            return (
              <div>
                {
                  "you shouldn't be seeing this message, please inform if you do"
                }
              </div>
            );
          }
        }
      })}
    </React.Fragment>
  );
};

export type { IFilter };
export { Filters, useFilters };
