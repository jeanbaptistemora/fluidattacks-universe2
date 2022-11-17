/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { faFilter } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback, useEffect, useState } from "react";

import type {
  IFilter,
  IFilterComp,
  IFiltersProps,
  IPermanentData,
} from "./types";

import { Button } from "components/Button";
import {
  FormikDate,
  FormikInput,
  FormikNumber,
  FormikSelect,
} from "components/Input/Formik";
import { Col, Row } from "components/Layout";
import { SidePanel } from "components/SidePanel";

const useFilters = <IData extends object>(
  data: IData[],
  filters: IFilter<IData>[]
): IData[] => {
  function handleTextSelectCases(
    dataPoint: IData,
    filter: IFilterComp<IData>
  ): boolean {
    if (filter.value === "" || filter.value === undefined) return true;

    switch (filter.filterFn) {
      case "caseSensitive":
        return String(dataPoint[filter.key]) === filter.value;

      case "caseInsensitive":
        return (
          String(dataPoint[filter.key]).toLowerCase() ===
          filter.value.toLowerCase()
        );

      case "includesSensitive":
        return String(dataPoint[filter.key]).includes(filter.value);

      case "includesInArray": {
        const array: unknown[] = JSON.parse(
          JSON.stringify(dataPoint[filter.key])
        );

        return array.includes(filter.value);
      }

      case "includesInsensitive":
      default:
        return String(dataPoint[filter.key])
          .toLowerCase()
          .includes(filter.value.toLowerCase());
    }
  }

  function handleNumberCase(
    dataPoint: IData,
    filter: IFilterComp<IData>
  ): boolean {
    return _.isEmpty(filter.value)
      ? true
      : String(dataPoint[filter.key]) === filter.value;
  }

  function handleNumberRangeCase(
    dataPoint: IData,
    filter: IFilterComp<IData>
  ): boolean {
    if (filter.rangeValues === undefined) return true;
    const currentNumber = parseInt(String(dataPoint[filter.key]), 10);
    const isHigher = _.isEmpty(filter.rangeValues[0])
      ? true
      : currentNumber >= parseInt(filter.rangeValues[0], 10);
    const isLower = _.isEmpty(filter.rangeValues[1])
      ? true
      : currentNumber <= parseInt(filter.rangeValues[1], 10);

    return isLower && isHigher;
  }

  function handleDateRangeCase(
    dataPoint: IData,
    filter: IFilterComp<IData>
  ): boolean {
    if (filter.rangeValues === undefined) return true;
    const currentDate = Date.parse(String(dataPoint[filter.key]));
    const isHigher = _.isEmpty(filter.rangeValues[0])
      ? true
      : currentDate >= Date.parse(filter.rangeValues[0]);
    const isLower = _.isEmpty(filter.rangeValues[1])
      ? true
      : currentDate <= Date.parse(filter.rangeValues[1]);

    return isHigher && isLower;
  }

  function checkAllFilters(dataPoint: IData): boolean {
    return filters.every((filter): boolean => {
      if (typeof filter.key === "function")
        return filter.key(dataPoint, filter.value, filter.rangeValues);
      switch (filter.type) {
        case "number":
          return handleNumberCase(dataPoint, filter as IFilterComp<IData>);

        case "numberRange":
          return handleNumberRangeCase(dataPoint, filter as IFilterComp<IData>);

        case "dateRange":
          return handleDateRangeCase(dataPoint, filter as IFilterComp<IData>);

        case "text":
        case "select":
        default:
          return handleTextSelectCases(dataPoint, filter as IFilterComp<IData>);
      }
    });
  }

  return data.filter((entry: IData): boolean => checkAllFilters(entry));
};

const Filters = <IData extends object>({
  dataset = undefined,
  permaset = undefined,
  filters,
  setFilters,
}: IFiltersProps<IData>): JSX.Element => {
  const [open, setOpen] = useState(false);

  const openPanel = useCallback((): void => {
    setOpen(true);
  }, []);
  const closePanel = useCallback((): void => {
    setOpen(false);
  }, []);

  const [permaValues, setPermaValues] = permaset ?? [undefined, undefined];

  function resetFiltersHandler(): (event: React.FormEvent) => void {
    return (event: React.FormEvent): void => {
      setFilters(
        filters.map((filter: IFilter<IData>): IFilter<IData> => {
          return { ...filter, rangeValues: ["", ""], value: "" };
        })
      );
      if (permaValues !== undefined) {
        setPermaValues(
          permaValues.map((permadata): IPermanentData => {
            return { ...permadata, rangeValues: ["", ""], value: "" };
          })
        );
      }
      event.stopPropagation();
    };
  }

  function onRangeValueChangeHandler(
    id: string,
    position: 0 | 1
  ): (event: React.ChangeEvent<HTMLInputElement>) => void {
    return (event: React.ChangeEvent<HTMLInputElement>): void => {
      setFilters(
        filters.map((filter): IFilter<IData> => {
          const value: [string, string] =
            position === 0
              ? [event.target.value, filter.rangeValues?.[1] ?? ""]
              : [filter.rangeValues?.[0] ?? "", event.target.value];
          if (filter.id === id) {
            return {
              ...filter,
              rangeValues: value,
            };
          }

          setPermaValues?.(
            permaValues.map((permadata): IPermanentData => {
              if (permadata.id === id) {
                return {
                  ...permadata,
                  rangeValues: value,
                };
              }

              return permadata;
            })
          );

          return filter;
        })
      );
    };
  }

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

          setPermaValues?.(
            permaValues.map((permadata): IPermanentData => {
              if (permadata.id === id) {
                return {
                  ...permadata,
                  value: event.target.value,
                };
              }

              return permadata;
            })
          );

          return filter;
        })
      );
    };
  }

  useEffect((): void => {
    if (permaset === undefined) return;
    setFilters(
      filters.map((filter): IFilter<IData> => {
        const permaValue = permaValues?.find(
          (permadata): boolean => permadata.id === filter.id
        );

        return {
          ...filter,
          rangeValues: permaValue?.rangeValues ?? filter.rangeValues,
          value: permaValue?.value ?? filter.value,
        };
      })
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <React.Fragment>
      <Button id={"filter-config"} onClick={openPanel} variant={"ghost"}>
        <div style={{ width: "55px" }} />
        <FontAwesomeIcon icon={faFilter} />
        &nbsp;
        {"Filter"}
      </Button>
      <SidePanel onClose={closePanel} open={open}>
        <React.Fragment>
          {filters.map((filter: IFilter<IData>): JSX.Element => {
            switch (filter.type) {
              case "text": {
                return (
                  <Row>
                    <Col>
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
                    </Col>
                  </Row>
                );
              }
              case "number": {
                return (
                  <Row>
                    <Col>
                      <FormikNumber
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
                    </Col>
                  </Row>
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
                          onChange: onRangeValueChangeHandler(filter.id, 0),
                          value: filter.rangeValues?.[0] ?? "",
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
                          onChange: onRangeValueChangeHandler(filter.id, 1),
                          value: filter.rangeValues?.[1] ?? "",
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
                const options =
                  typeof filter.selectOptions === "function"
                    ? filter.selectOptions(dataset ?? [])
                    : filter.selectOptions;

                return (
                  <Row>
                    <Col>
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
                        {options?.map((option): JSX.Element => {
                          if (typeof option === "string") {
                            return (
                              <option key={option} value={option}>
                                {option}
                              </option>
                            );
                          }

                          return (
                            <option key={option.value} value={option.value}>
                              {option.header}
                            </option>
                          );
                        })}
                      </FormikSelect>
                    </Col>
                  </Row>
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
                          onChange: onRangeValueChangeHandler(filter.id, 0),
                          value: filter.rangeValues?.[0] ?? "",
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
                          onChange: onRangeValueChangeHandler(filter.id, 1),
                          value: filter.rangeValues?.[1] ?? "",
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
                return <div />;
              }
            }
          })}
          <Row>
            <Col>
              <Button onClick={resetFiltersHandler()} variant={"secondary"}>
                {"Clear filters"}
              </Button>
            </Col>
          </Row>
        </React.Fragment>
      </SidePanel>
    </React.Fragment>
  );
};

export type { IFilter, IPermanentData };
export { Filters, useFilters };
