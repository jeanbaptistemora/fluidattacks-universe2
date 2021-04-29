import { Checkbox } from "antd";
import type { FieldProps } from "formik";
import React from "react";
import "./index.css";

import { ValidationError } from "styles/styledComponents";

interface ICheckboxProps extends FieldProps {
  children: React.ReactNode;
  label: string;
}

export const FormikCheckbox: React.FC<ICheckboxProps> = (
  props: ICheckboxProps
): JSX.Element => {
  const { field, form, children, label } = props;
  const { name, value } = field;
  const { touched, errors } = form;
  const error = errors[name];
  const fieldTouched = Boolean(touched[name]);

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
      {fieldTouched && error !== undefined ? (
        <ValidationError id={"validationError"}>
          {error as string}
        </ValidationError>
      ) : undefined}
    </React.Fragment>
  );
};
