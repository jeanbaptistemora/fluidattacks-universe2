import type { Column, RowData } from "@tanstack/react-table";
import _ from "lodash";
import React, { useMemo } from "react";

import { FormikSelect } from "components/Input/Formik";

interface ISelectFilterProps<TData extends RowData> {
  column: Column<TData, unknown>;
}

const SelectFilter = <TData extends RowData>({
  column,
}: ISelectFilterProps<TData>): JSX.Element => {
  const uniqueValues: Map<string, number> = column.getFacetedUniqueValues();
  const sortedUniqueValues = useMemo(
    (): string[] => _.sortBy(Array.from(uniqueValues.keys())),
    [uniqueValues]
  );

  return (
    <div>
      <FormikSelect
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
        name={column.id}
      >
        <option value={""}>{"All"}</option>
        {sortedUniqueValues
          .flatMap((value): string => value)
          .filter(
            (value, index, arr): boolean =>
              arr.indexOf(value) === index && Boolean(value) && value !== "-"
          )
          .map(
            (value): JSX.Element => (
              <option key={value} value={value}>
                {value}
              </option>
            )
          )}
      </FormikSelect>
    </div>
  );
};

export { SelectFilter };
