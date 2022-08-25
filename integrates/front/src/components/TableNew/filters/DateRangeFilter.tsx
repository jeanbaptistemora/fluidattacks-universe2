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
  const filterValue = column.getFilterValue() as [string, string] | undefined;
  const currentValue =
    filterValue === undefined ? [undefined, undefined] : filterValue;

  const handleMinChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>): void => {
      column.setFilterValue(
        (
          old: [string, string] | undefined
        ): [string | undefined, string | undefined] => [
          event.target.value === "" ? undefined : event.target.value,
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
          old: [string, string] | undefined
        ): [string | undefined, string | undefined] => [
          old === undefined ? undefined : old[0],
          event.target.value === "" ? undefined : event.target.value,
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
            value: currentValue[0] ?? "",
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
            value: currentValue[1] ?? "",
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
