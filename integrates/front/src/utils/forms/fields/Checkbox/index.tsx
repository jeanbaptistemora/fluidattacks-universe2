import _ from "lodash";
import React from "react";
import type { WrappedFieldProps } from "redux-form";

import { ValidationError } from "styles/styledComponents";

interface ICheckboxProps extends WrappedFieldProps {
  children: React.ReactNode;
}

export const Checkbox: React.FC<ICheckboxProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: ICheckboxProps
): JSX.Element => {
  const { input, meta, children } = props;
  const { value } = input;
  const { touched, error } = meta;

  return (
    <React.Fragment>
      <input
        checked={value}
        type={"checkbox"}
        // Best way to pass down props.
        // eslint-disable-next-line react/jsx-props-no-spreading
        {...input}
      />
      {children}
      {touched && !_.isUndefined(error) && (
        <ValidationError
          // We need it to override default styles from react-bootstrap.
          // eslint-disable-next-line react/forbid-component-props
          id={"validationError"}
        >
          {error as string}
        </ValidationError>
      )}
    </React.Fragment>
  );
};
