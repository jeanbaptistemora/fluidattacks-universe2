/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { Column, RowData } from "@tanstack/react-table";
import React, { useCallback } from "react";

import { FormikDate } from "components/Input/Formik";
import { Col, Row } from "components/Layout";

interface IDateRangeFilterProps<TData extends RowData> {
  column: Column<TData, unknown>;
}

const DateRangeFilter = <TData extends RowData>({
  column,
}: IDateRangeFilterProps<TData>): JSX.Element => {
  const filterValue = column.getFilterValue() as [number, number] | undefined;
  const currentValue =
    filterValue === undefined ? [undefined, undefined] : filterValue;

  const handleMinChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>): void => {
      column.setFilterValue(
        (
          old: [number, number] | undefined
        ): [number | undefined, number | undefined] => [
          event.target.value === ""
            ? undefined
            : Date.parse(event.target.value),
          old === undefined ? undefined : old[1],
        ]
      );
    },
    [column]
  );

  const handleMaxChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>): void => {
      column.setFilterValue(
        (
          old: [number, number] | undefined
        ): [number | undefined, number | undefined] => [
          old === undefined ? undefined : old[0],
          event.target.value === ""
            ? undefined
            : Date.parse(event.target.value),
        ]
      );
    },
    [column]
  );

  return (
    <Row>
      <Col lg={50} md={50}>
        <FormikDate
          field={{
            name: column.id,
            onBlur: (): void => undefined,
            onChange: handleMinChange,
            value:
              currentValue[0] === undefined
                ? ""
                : new Date(currentValue[0]).toISOString().split("T")[0],
          }}
          form={{ errors: {}, touched: {} }}
          label={column.columnDef.header}
          name={column.id}
        />
      </Col>
      <Col lg={50} md={50}>
        <FormikDate
          field={{
            name: column.id,
            onBlur: (): void => undefined,
            onChange: handleMaxChange,
            value:
              currentValue[1] === undefined
                ? ""
                : new Date(currentValue[1]).toISOString().split("T")[0],
          }}
          form={{ errors: {}, touched: {} }}
          label={""}
          name={column.id}
        />
      </Col>
    </Row>
  );
};

export { DateRangeFilter };
