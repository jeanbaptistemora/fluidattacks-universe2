/* eslint-disable @typescript-eslint/prefer-readonly-parameter-types, react/forbid-component-props
  -------
  Readonly utility type does not work on deeply nested types and we need
  className to override default styles from react-bootstrap.
*/
import React from "react";
import { WrappedFieldProps } from "redux-form";
import _ from "lodash";
import { default as style } from "../../index.css";
import { FormControl, FormControlProps, HelpBlock } from "react-bootstrap";

export const Dropdown: React.FC<WrappedFieldProps & FormControlProps> = (
  props: WrappedFieldProps & FormControlProps
): JSX.Element => {
  const { input, meta, children } = props;
  const { initial, touched, error } = meta;
  const { onChange } = input;

  function handleDropdownChange(event: React.FormEvent<FormControl>): void {
    onChange((event.target as HTMLInputElement).value);
  }

  return (
    <React.Fragment>
      <FormControl
        className={style.formControl}
        componentClass={"select"}
        defaultValue={initial}
        onChange={handleDropdownChange}
      >
        {children}
      </FormControl>
      {touched && !_.isUndefined(error) && (
        <HelpBlock className={style.validationError} id={"validationError"}>
          {error as string}
        </HelpBlock>
      )}
    </React.Fragment>
  );
};
