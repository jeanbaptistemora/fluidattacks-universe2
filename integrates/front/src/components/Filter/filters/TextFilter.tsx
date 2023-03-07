/* eslint-disable react/require-default-props */
import React, { useState } from "react";

import { FormikInput } from "components/Input/Formik";
import { Col, Row } from "components/Layout";

interface ITextFilterProps {
  id: string;
  label: string;
  onChange: (id: string, value: string) => void;
  value?: string;
}

const TextFilter = ({
  id,
  label,
  onChange,
  value,
}: ITextFilterProps): JSX.Element => {
  const [textValue, setTextValue] = useState(value);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const eventValue = event.target.value;
    setTextValue(eventValue);
    onChange(id, eventValue);
  };

  return (
    <Row key={id}>
      <Col>
        <FormikInput
          field={{
            name: id,
            onBlur: (): void => undefined,
            onChange: handleChange,
            value: textValue ?? "",
          }}
          form={{ errors: {}, touched: {} }}
          label={label}
          name={id}
        />
      </Col>
    </Row>
  );
};

export { TextFilter };
