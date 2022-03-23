/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
 */
import { Checkbox } from "antd";
import type { FieldProps } from "formik";
import { ErrorMessage } from "formik";
import React from "react";

import { ValidationError } from "utils/forms/fields/styles";

interface ICheckboxProps extends FieldProps {
  children: React.ReactNode;
  isChecked?: boolean;
  label: string;
}

export const FormikCheckbox: React.FC<ICheckboxProps> = (
  props: Readonly<ICheckboxProps>
): JSX.Element => {
  const { field, children, isChecked = false, label } = props;
  const { name, value } = field;

  return (
    <React.Fragment>
      {isChecked ? (
        <Checkbox
          aria-label={name}
          checked={true}
          // Best way to pass down props.
          // eslint-disable-next-line react/jsx-props-no-spreading
          {...props}
        >
          {` ${label}`}
        </Checkbox>
      ) : (
        <Checkbox
          aria-label={name}
          checked={value}
          // Best way to pass down props.
          // eslint-disable-next-line react/jsx-props-no-spreading
          {...field}
        >
          {` ${label}`}
        </Checkbox>
      )}

      {children}
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};
