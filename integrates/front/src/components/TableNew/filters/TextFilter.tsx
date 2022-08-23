import type { Column, RowData } from "@tanstack/react-table";
import React from "react";

import { FormikInput } from "components/Input/Formik";

interface ITextFilterProps<TData extends RowData> {
  column: Column<TData, unknown>;
}

const TextFilter = <TData extends RowData>({
  column,
}: ITextFilterProps<TData>): JSX.Element => {
  return (
    <div>
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
        name={column.id}
      />
    </div>
  );
};

export { TextFilter };
