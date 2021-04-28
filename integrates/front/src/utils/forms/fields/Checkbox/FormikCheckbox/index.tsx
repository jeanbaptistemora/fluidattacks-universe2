import type { FieldProps } from "formik";
import React from "react";

import { ValidationError } from "styles/styledComponents";

interface ICheckboxProps extends FieldProps {
  children: React.ReactNode;
}

export const FormikCheckbox: React.FC<ICheckboxProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: ICheckboxProps
): JSX.Element => {
  const { field, form, children } = props;
  const { name, value } = field;
  const { touched, errors } = form;
  const error = errors[name];
  const fieldTouched = Boolean(touched[name]);

  return (
    <React.Fragment>
      <input
        checked={value}
        type={"checkbox"}
        // Best way to pass down props.
        // eslint-disable-next-line react/jsx-props-no-spreading
        {...field}
      />
      {children}
      {fieldTouched && error !== undefined ? (
        <ValidationError
          // We need it to override default styles from react-bootstrap.
          // eslint-disable-next-line react/forbid-component-props
          id={"validationError"}
        >
          {error as string}
        </ValidationError>
      ) : undefined}
    </React.Fragment>
  );
};
