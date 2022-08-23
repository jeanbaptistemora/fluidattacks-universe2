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
  const filterValue = column.getFilterValue() as [number, number] | null;
  const currentValue: [number, number] =
    filterValue === null ? [0, 0] : filterValue;

  return (
    <React.Fragment>
      <FormikNumber
        field={{
          name: column.id,
          onBlur: (): void => undefined,
          onChange: (event: React.ChangeEvent<HTMLInputElement>): void => {
            column.setFilterValue(
              (old: [number, number] | null): [number, number] => [
                Number(event.target.value),
                old === null ? 0 : old[1],
              ]
            );
          },
          value: String(currentValue[0]),
        }}
        form={{ errors: {}, touched: {} }}
        label={column.columnDef.header}
        max={minMaxValues === undefined ? undefined : minMaxValues[1]}
        min={minMaxValues === undefined ? undefined : minMaxValues[0]}
        name={column.id}
      />
      <FormikNumber
        field={{
          name: column.id,
          onBlur: (): void => undefined,
          onChange: (event: React.ChangeEvent<HTMLInputElement>): void => {
            column.setFilterValue(
              (old: [number, number] | null): [number, number] => [
                old === null ? 0 : old[0],
                Number(event.target.value),
              ]
            );
          },
          value: String(currentValue[1]),
        }}
        form={{ errors: {}, touched: {} }}
        label={column.columnDef.header}
        max={minMaxValues === undefined ? undefined : minMaxValues[1]}
        min={minMaxValues === undefined ? undefined : minMaxValues[0]}
        name={column.id}
      />
    </React.Fragment>
  );
};

export { NumberFilter };
