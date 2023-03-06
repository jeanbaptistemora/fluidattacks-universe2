/* eslint-disable react/require-default-props */
import React, { useState } from "react";

import { FormikDate } from "components/Input/Formik";
import { Col, Row } from "components/Layout";

interface IDateRangeProps {
  id: string;
  label: string;
  onChange: (id: string, rangeValues: [string, string]) => void;
  numberRangeValues?: [string, string];
}

const DateRange = ({
  id,
  label,
  onChange,
  numberRangeValues = undefined,
}: IDateRangeProps): JSX.Element => {
  const [rangeValues, setRangeValues] = useState(numberRangeValues);

  const handleChange = (
    position: 0 | 1
  ): ((event: React.ChangeEvent<HTMLInputElement>) => void) => {
    return (event: React.ChangeEvent<HTMLInputElement>): void => {
      const value: [string, string] =
        position === 0
          ? [event.target.value, rangeValues?.[1] ?? ""]
          : [rangeValues?.[0] ?? "", event.target.value];
      setRangeValues(value);
      onChange(id, value);
    };
  };

  return (
    <Row key={id}>
      <Col lg={50} md={50}>
        <FormikDate
          field={{
            name: id,
            onBlur: (): void => undefined,
            onChange: handleChange(0),
            value: rangeValues?.[0] ?? "",
          }}
          form={{ errors: {}, touched: {} }}
          label={label}
          name={id}
        />
      </Col>
      <Col lg={50} md={50}>
        <FormikDate
          field={{
            name: id,
            onBlur: (): void => undefined,
            onChange: handleChange(1),
            value: rangeValues?.[1] ?? "",
          }}
          form={{ errors: {}, touched: {} }}
          label={""}
          name={id}
        />
      </Col>
    </Row>
  );
};

export { DateRange };
