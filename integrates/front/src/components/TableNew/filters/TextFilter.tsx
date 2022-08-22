import type { Column, RowData } from "@tanstack/react-table";
import _ from "lodash";
import React, { useMemo } from "react";

import { FormikInput } from "components/Input/Formik";

interface ITextFilterProps<TData extends RowData> {
  column: Column<TData, unknown>;
}

const TextFilter = <TData extends RowData>({
  column,
}: ITextFilterProps<TData>): JSX.Element => {
  const uniqueValues: Map<string, number> = column.getFacetedUniqueValues();
  const sortedUniqueValues = useMemo(
    (): string[] => _.sortBy(Array.from(uniqueValues.keys())),
    [uniqueValues]
  );

  return (
    <React.Fragment>
      <datalist id={`${column.id}-list`}>
        {sortedUniqueValues.map(
          (value): JSX.Element => (
            <option key={value} value={value} />
          )
        )}
      </datalist>
      <FormikInput
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
        list={`${column.id}-list`}
        name={column.id}
      >
        {column.id}
      </FormikInput>
    </React.Fragment>
  );
};

export { TextFilter };
