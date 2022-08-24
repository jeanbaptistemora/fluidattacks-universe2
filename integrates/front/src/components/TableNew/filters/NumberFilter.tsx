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

  return (
    <div>
      <FormikNumber
        field={{
          name: column.id,
          onBlur: (): void => undefined,
          onChange: (event: React.ChangeEvent<HTMLInputElement>): void => {
            column.setFilterValue(event.target.value);
          },
          value: (column.getFilterValue() ?? "") as string,
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
