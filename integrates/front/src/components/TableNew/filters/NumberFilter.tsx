/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { Column, RowData } from "@tanstack/react-table";
import React from "react";

import { FormikNumber } from "components/Input/Formik";

interface INumberFilterProps<TData extends RowData> {
  column: Column<TData, unknown>;
}

const NumberFilter = <TData extends RowData>({
  column,
}: INumberFilterProps<TData>): JSX.Element => {
  const minMaxValues = column.getFacetedMinMaxValues();
  const maxValue = minMaxValues === undefined ? undefined : minMaxValues[1];
  const filterValue = column.getFilterValue() as [number, number] | undefined;
  const currentValue =
    filterValue === undefined ? [undefined, undefined] : filterValue;

  return (
    <div>
      <FormikNumber
        field={{
          name: column.id,
          onBlur: (): void => undefined,
          onChange: (event: React.ChangeEvent<HTMLInputElement>): void => {
            column.setFilterValue([Number(event.target.value), maxValue]);
          },
          value: currentValue[0] === undefined ? "" : String(currentValue[0]),
        }}
        form={{ errors: {}, touched: {} }}
        label={column.columnDef.header}
        max={maxValue}
        min={0}
        name={column.id}
      />
    </div>
  );
};

export { NumberFilter };
