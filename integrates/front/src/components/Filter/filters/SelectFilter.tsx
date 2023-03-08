/* eslint-disable react/require-default-props */
import React, { useState } from "react";

import type { ISelectedOptions } from "../types";
import { FormikSelect } from "components/Input/Formik";
import { Col, Row } from "components/Layout";

interface ISelectFilterProps {
  id: string;
  label: string;
  onChange: (id: string, value: string) => void;
  mappedOptions?: ISelectedOptions[];
  value?: string;
}

const SelectFilter = ({
  id,
  label,
  mappedOptions = [],
  onChange,
  value = "",
}: ISelectFilterProps): JSX.Element => {
  const [selectValue, setSelectValue] = useState(value);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const eventValue = event.target.value;
    setSelectValue(eventValue);
    onChange(id, eventValue);
  };

  return (
    <Row key={id}>
      <Col>
        <FormikSelect
          field={{
            name: id,
            onBlur: (): void => undefined,
            onChange: handleChange,
            value: selectValue,
          }}
          form={{ errors: {}, touched: {} }}
          label={label}
          name={id}
        >
          <option value={""}>{"All"}</option>
          {mappedOptions.map((option): JSX.Element => {
            return (
              <option key={option.value} value={option.value}>
                {option.header}
              </option>
            );
          })}
        </FormikSelect>
      </Col>
    </Row>
  );
};

export { SelectFilter };
