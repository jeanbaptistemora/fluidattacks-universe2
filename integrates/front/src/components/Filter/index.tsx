import { faFilter } from "@fortawesome/free-solid-svg-icons";
import _ from "lodash";
import React, { useCallback, useEffect, useState } from "react";

import { AppliedFilters } from "./AppliedFilters";
import type {
  IFilter,
  IFilterComp,
  IFiltersProps,
  IPermanentData,
} from "./types";
import { getMappedOptions } from "./utils";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Label } from "components/Input";
import {
  FormikCheckbox,
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

  function handleCheckBoxesCase(
    dataPoint: IData,
    filter: IFilterComp<IData>
  ): boolean {
    if (_.isEmpty(filter.checkValues)) return true;

    return filter.checkValues?.includes(String(dataPoint[filter.key])) ?? true;
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

        case "checkBoxes":
          return handleCheckBoxesCase(dataPoint, filter as IFilterComp<IData>);

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

  function setPermanentValues({
    id,
    value,
    rangeValues,
    checkValues,
  }: IPermanentData): void {
    setPermaValues?.(
      permaValues.map((permadata): IPermanentData => {
        if (permadata.id === id) {
          return {
            ...permadata,
            checkValues,
            rangeValues,
            value,
          };
        }

        return permadata;
      })
    );
  }

  const removeFilter = useCallback(
    (filterToReset: IFilter<IData>): (() => void) => {
      return (): void => {
        setFilters(
          filters.map((filter: IFilter<IData>): IFilter<IData> => {
            if (filter.id === filterToReset.id) {
              return {
                ...filter,
                checkValues: [],
                rangeValues: ["", ""],
                value: "",
              };
            }

            return {
              ...filter,
            };
          })
        );
        setPermaValues?.(
          permaValues.map((permadata): IPermanentData => {
            if (permadata.id === filterToReset.id) {
              return {
                ...permadata,
                checkValues: [],
                rangeValues: ["", ""],
                value: "",
              };
            }

            return {
              ...permadata,
            };
          })
        );
      };
    },
    [filters, permaValues, setFilters, setPermaValues]
  );

  function resetFiltersHandler(): (event: React.FormEvent) => void {
    return (event: React.FormEvent): void => {
      setFilters(
        filters.map((filter: IFilter<IData>): IFilter<IData> => {
          return {
            ...filter,
            checkValues: [],
            rangeValues: ["", ""],
            value: "",
          };
        })
      );
      setPermaValues?.(
        permaValues.map((permadata): IPermanentData => {
          return {
            ...permadata,
            checkValues: [],
            rangeValues: ["", ""],
            value: "",
          };
        })
      );
      event.stopPropagation();
    };
  }

  function onCheckValuesChangeHadler(
    id: string
  ): (event: React.ChangeEvent<HTMLInputElement>) => void {
    const temp = (event: React.ChangeEvent<HTMLInputElement>): void => {
      setFilters(
        filters.map((filter): IFilter<IData> => {
          if (filter.id === id) {
            const filtersCheckvalues = filter.checkValues
              ? filter.checkValues
              : [];
            const checkValues = filtersCheckvalues.includes(event.target.value)
              ? filtersCheckvalues.filter(
                  (option): boolean => option !== event.target.value
                )
              : [...filtersCheckvalues, event.target.value];

            setPermanentValues({
              checkValues,
              id,
              rangeValues: filter.rangeValues,
              value: filter.value,
            });

            return {
              ...filter,
              checkValues,
            };
          }

          return filter;
        })
      );
    };

    return temp;
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
            setPermanentValues({
              checkValues: filter.checkValues,
              id,
              rangeValues: value,
              value: filter.value,
            });

            return {
              ...filter,
              rangeValues: value,
            };
          }

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
            setPermanentValues({
              checkValues: filter.checkValues,
              id,
              rangeValues: filter.rangeValues,
              value: event.target.value,
            });

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

  useEffect((): void => {
    if (permaset === undefined) return;
    setFilters(
      filters.map((filter): IFilter<IData> => {
        const permaValue = permaValues?.find(
          (permadata): boolean => permadata.id === filter.id
        );

        return {
          ...filter,
          checkValues: permaValue?.checkValues ?? filter.checkValues,
          rangeValues: permaValue?.rangeValues ?? filter.rangeValues,
          value: permaValue?.value ?? filter.value,
        };
      })
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <React.Fragment>
      <Container align={"center"} display={"flex"} pb={"4px"} wrap={"wrap"}>
        <Container pr={"4px"}>
          <Button
            icon={faFilter}
            id={"filter-config"}
            onClick={openPanel}
            variant={"ghost"}
          >
            {"Filter"}
          </Button>
        </Container>
        <AppliedFilters
          dataset={dataset}
          filters={filters as IFilter<object>[]}
          onClose={removeFilter}
        />
      </Container>
      <SidePanel onClose={closePanel} open={open}>
        <React.Fragment>
          {filters.map((filter: IFilter<IData>): JSX.Element => {
            const mappedOptions = getMappedOptions(
              filter as IFilter<object>,
              dataset
            );

            switch (filter.type) {
              case "text": {
                return (
                  <Row key={filter.id}>
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
                  <Row key={filter.id}>
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
                  <Row key={filter.id}>
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
                return (
                  <Row key={filter.id}>
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
                        {mappedOptions?.map((option): JSX.Element => {
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
                  <Row key={filter.id}>
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
              case "checkBoxes": {
                return (
                  <Row key={filter.id}>
                    <Label> {filter.label} </Label>
                    {mappedOptions?.map((option): JSX.Element => {
                      return (
                        <Col key={option.value}>
                          <FormikCheckbox
                            field={{
                              checked: filter.checkValues?.includes(
                                option.value
                              ),
                              name: option.value,
                              onBlur: (): void => undefined,
                              onChange: onCheckValuesChangeHadler(filter.id),
                              value: option.value,
                            }}
                            form={{ errors: {}, touched: {} }}
                            label={option.header}
                            name={option.value}
                            value={option.value}
                          />
                        </Col>
                      );
                    })}
                  </Row>
                );
              }
              default: {
                return <div key={filter.id} />;
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
