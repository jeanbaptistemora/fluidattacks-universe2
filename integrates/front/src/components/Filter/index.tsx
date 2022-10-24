/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";
import type { Dispatch, SetStateAction } from "react";

import {
  FormikDate,
  FormikInput,
  FormikNumber,
  FormikSelect,
} from "components/Input/Formik";
import { Col, Row } from "components/Layout";

interface IFilter {
  id: string;
  label?: string;
  rangeValues?: [string | undefined, string | undefined];
  selectOptions?: string[];
  type: "dateRange" | "number" | "numberRange" | "select" | "text";
  value?: string;
}

interface IFiltersProps {
  filters: IFilter[];
  setFilters: Dispatch<SetStateAction<IFilter[]>>;
}

export const Filters = ({
  filters,
  setFilters,
}: IFiltersProps): JSX.Element => {
  function onValueChangeHandler(
    id: string
  ): (event: React.ChangeEvent<HTMLInputElement>) => void {
    return (event: React.ChangeEvent<HTMLInputElement>): void => {
      setFilters(
        filters.map((filter): IFilter => {
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
      {filters.map((filter: IFilter): JSX.Element => {
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
                  value:
                    filter.rangeValues?.[0] === undefined
                      ? ""
                      : String(filter.rangeValues[0]),
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
