/* eslint-disable react/forbid-component-props
  -------
  We need it to override default styles from react-bootstrap
*/
import _ from "lodash";
import React from "react";
import type { WrappedFieldProps } from "redux-form";

import { ValidationError } from "styles/styledComponents";
import style from "utils/forms/index.css";

interface ITextProps extends WrappedFieldProps {
  disabled?: boolean;
  id?: string;
  max?: number | string;
  min?: number | string;
  placeholder?: string;
  type?: string;
}

export const Text: React.FC<ITextProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<ITextProps>
): JSX.Element => {
  const { disabled, id, max, min, input, placeholder, type, meta } = props;
  const { name, onBlur, onChange, value } = input;

  return (
    <React.Fragment>
      <input
        className={style["form-control"]}
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
        <ValidationError id={"validationError"}>
          {meta.error as string}
        </ValidationError>
      )}
    </React.Fragment>
  );
};
