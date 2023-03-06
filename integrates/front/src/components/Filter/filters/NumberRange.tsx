/* eslint-disable react/require-default-props */
import React, { useState } from "react";

import { FormikNumber } from "components/Input/Formik";
import { Col, Row } from "components/Layout";

interface INumberRangeProps {
  id: string;
  label: string;
  onChange: (id: string, rangeValues: [string, string]) => void;
  numberRangeValues?: [string, string];
}

const NumberRange = ({
  id,
  label,
  onChange,
  numberRangeValues,
}: INumberRangeProps): JSX.Element => {
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
        <FormikNumber
          field={{
            name: id,
            onBlur: (): void => undefined,
            onChange: handleChange(0),
            value: rangeValues?.[0] ?? "",
          }}
          form={{ errors: {}, touched: {} }}
          label={label}
          name={id}
          placeholder={"Min"}
        />
      </Col>
      <Col lg={50} md={50}>
        <FormikNumber
          field={{
            name: id,
            onBlur: (): void => undefined,
            onChange: handleChange(1),
            value: rangeValues?.[1] ?? "",
          }}
          form={{ errors: {}, touched: {} }}
          label={""}
          name={id}
          placeholder={"Max"}
        />
      </Col>
    </Row>
  );
};

export { NumberRange };
