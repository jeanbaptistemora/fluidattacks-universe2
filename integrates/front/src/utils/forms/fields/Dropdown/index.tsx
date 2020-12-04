/* eslint-disable @typescript-eslint/prefer-readonly-parameter-types, react/forbid-component-props
  -------
  Readonly utility type does not work on deeply nested types and we need
  className to override default styles from react-bootstrap.
*/
import type { FormControlProps } from "react-bootstrap";
import React from "react";
import type { WrappedFieldProps } from "redux-form";
import _ from "lodash";
import style from "utils/forms/index.css";
import { FormControl, HelpBlock } from "react-bootstrap";

export const Dropdown: React.FC<WrappedFieldProps & FormControlProps> = (
  props: WrappedFieldProps & FormControlProps
): JSX.Element => {
  const { input, meta, children } = props;
  const { initial, touched, error } = meta;
  const { name, onChange } = input;

  function handleDropdownChange(event: React.FormEvent<FormControl>): void {
    onChange((event.target as HTMLInputElement).value);
  }

  return (
    <React.Fragment>
      <FormControl
        className={style["form-control"]}
        componentClass={"select"}
        defaultValue={initial}
        name={name}
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
