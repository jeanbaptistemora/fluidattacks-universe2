/* eslint-disable react/require-default-props */
import React, { useState } from "react";

import type { ISelectedOptions } from "../types";
import { Label } from "components/Input";
import { FormikCheckbox } from "components/Input/Formik";
import { Col, Row } from "components/Layout";

interface ITextFilterProps {
  id: string;
  label: string;
  onChange: (id: string, value: string[]) => void;
  checkValues?: string[];
  mappedOptions?: ISelectedOptions[];
}

const CheckBoxFilter = ({
  checkValues = [],
  id,
  label,
  mappedOptions,
  onChange,
}: ITextFilterProps): JSX.Element => {
  const [checkBoxValues, setCheckBoxValues] = useState(checkValues);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const { value } = event.target;
    const isChecked = event.target.checked;
    const newValues = isChecked
      ? [...checkBoxValues, value]
      : checkBoxValues.filter((option): boolean => option !== value);
    setCheckBoxValues(newValues);
    onChange(id, newValues);
  };

  return (
    <Row key={id}>
      <Label> {label} </Label>
      {mappedOptions?.map((option): JSX.Element => {
        return (
          <Col key={option.value}>
            <FormikCheckbox
              field={{
                checked: checkBoxValues.includes(option.value),
                name: option.value,
                onBlur: (): void => undefined,
                onChange: handleChange,
                value: option.value,
              }}
              form={{ errors: {}, touched: {} }}
              label={option.header}
              name={option.value}
              value={option.value}
            />
          </Col>
        );
      })}
    </Row>
  );
};

export { CheckBoxFilter };
