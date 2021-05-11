import { Checkbox } from "antd";
import type { FieldProps } from "formik";
import { ErrorMessage } from "formik";
import React from "react";
import "antd/dist/antd.css";

import { ValidationError } from "utils/forms/fields/styles";

interface ICheckboxProps extends FieldProps {
  children: React.ReactNode;
  label: string;
}

export const FormikCheckbox: React.FC<ICheckboxProps> = (
  props: ICheckboxProps
): JSX.Element => {
  const { field, children, label } = props;
  const { name, value } = field;

  return (
    <React.Fragment>
      <Checkbox
        checked={value}
        // Best way to pass down props.
        // eslint-disable-next-line react/jsx-props-no-spreading
        {...field}
      >
        {` ${label}`}
      </Checkbox>
      {children}
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};
