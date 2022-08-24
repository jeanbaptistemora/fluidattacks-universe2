import type { Column, RowData } from "@tanstack/react-table";
import React, { useCallback } from "react";

import { FormikNumber } from "components/Input/Formik";
import { Col, Row } from "components/Layout";

interface INumberFilterProps<TData extends RowData> {
  column: Column<TData, unknown>;
}

const NumberRangeFilter = <TData extends RowData>({
  column,
}: INumberFilterProps<TData>): JSX.Element => {
  const minMaxValues = column.getFacetedMinMaxValues();
  const maxValue = minMaxValues === undefined ? undefined : minMaxValues[1];
  const filterValue = column.getFilterValue() as [number, number] | undefined;
  const currentValue =
    filterValue === undefined ? [undefined, undefined] : filterValue;

  const handleMinChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>): void => {
      column.setFilterValue(
        (
          old: [number, number] | undefined
        ): [number | undefined, number | undefined] => [
          event.target.value === "" ? undefined : Number(event.target.value),
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
          event.target.value === "" ? undefined : Number(event.target.value),
        ]
      );
    },
    [column]
  );

  return (
    <Row>
      <Col lg={50} md={50}>
        <FormikNumber
          field={{
            name: column.id,
            onBlur: (): void => undefined,
            onChange: handleMinChange,
            value: currentValue[0] === undefined ? "" : String(currentValue[0]),
          }}
          form={{ errors: {}, touched: {} }}
          label={column.columnDef.header}
          max={maxValue}
          min={0}
          name={column.id}
          placeholder={"Min"}
        />
      </Col>
      <Col lg={50} md={50}>
        <FormikNumber
          field={{
            name: column.id,
            onBlur: (): void => undefined,
            onChange: handleMaxChange,
            value: currentValue[1] === undefined ? "" : String(currentValue[1]),
          }}
          form={{ errors: {}, touched: {} }}
          label={""}
          max={maxValue}
          min={0}
          name={column.id}
          placeholder={"Max"}
        />
      </Col>
    </Row>
  );
};

export { NumberRangeFilter };
