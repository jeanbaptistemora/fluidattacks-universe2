/* eslint-disable react/require-default-props */
import React, { useState } from "react";

import { FormikNumber } from "components/Input/Formik";
import { Col, Row } from "components/Layout";

interface INumberFilterProps {
  id: string;
  label: string;
  onChange: (id: string, value: string) => void;
  value?: string;
}

const NumberFilter = ({
  id,
  label,
  onChange,
  value,
}: INumberFilterProps): JSX.Element => {
  const [numberValue, setNumberValue] = useState(value);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const eventValue = event.target.value;
    setNumberValue(eventValue);
    onChange(id, eventValue);
  };

  return (
    <Row key={id}>
      <Col>
        <FormikNumber
          field={{
            name: id,
            onBlur: (): void => undefined,
            onChange: handleChange,
            value: numberValue ?? "",
          }}
          form={{ errors: {}, touched: {} }}
          label={label}
          name={id}
        />
      </Col>
    </Row>
  );
};

export { NumberFilter };
