import React from "react";
import { WrappedFieldProps } from "redux-form";
import _ from "lodash";
import style from "utils/forms/index.css";
import {
  Checkbox as BootstrapCheckbox,
  FormControlProps,
  HelpBlock,
} from "react-bootstrap";

export const Checkbox: React.FC<WrappedFieldProps & FormControlProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: WrappedFieldProps & FormControlProps
): JSX.Element => {
  const { input, meta, children } = props;
  const { value } = input;
  const { touched, error } = meta;

  return (
    <React.Fragment>
      <BootstrapCheckbox
        checked={value}
        // Best way to pass down props.
        // eslint-disable-next-line react/jsx-props-no-spreading
        {...input}
      >
        {children}
      </BootstrapCheckbox>
      {touched && !_.isUndefined(error) && (
        <HelpBlock
          // We need it to override default styles from react-bootstrap.
          // eslint-disable-next-line react/forbid-component-props
          className={style.validationError}
          id={"validationError"}
        >
          {error as string}
        </HelpBlock>
      )}
    </React.Fragment>
  );
};
