/* eslint-disable react/forbid-component-props
  -------
  We need it to override default styles from react-bootstrap
*/
import type { FormControlProps } from "react-bootstrap";
import React from "react";
import type { WrappedFieldProps } from "redux-form";
import _ from "lodash";
import style from "utils/forms/index.css";
import { FormControl, HelpBlock } from "react-bootstrap";

export const Text: React.FC<WrappedFieldProps & FormControlProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<WrappedFieldProps & FormControlProps>
): JSX.Element => {
  const { disabled, id, max, min, input, placeholder, type, meta } = props;
  const { name, onBlur, onChange, value } = input;

  return (
    <React.Fragment>
      <FormControl
        className={style.formControl}
        disabled={disabled}
        id={id}
        max={max}
        min={min}
        name={name}
        onBlur={onBlur}
        onChange={onChange}
        placeholder={placeholder}
        type={type}
        value={value}
      />
      {meta.touched && !_.isUndefined(meta.error) && (
        <HelpBlock className={style.validationError} id={"validationError"}>
          {meta.error as string}
        </HelpBlock>
      )}
    </React.Fragment>
  );
};
