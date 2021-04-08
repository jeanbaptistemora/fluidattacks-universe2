/* eslint-disable react/forbid-component-props
  -------
  We need it to override default styles from react-bootstrap
*/
import type { FieldProps } from "formik";
import React from "react";

import style from "utils/forms/index.css";

interface ITextProps extends FieldProps {
  disabled: boolean;
  id: string;
  max: number | string;
  min: number | string;
  placeholder: string;
  type: string;
}

export const FormikText = (props: ITextProps): JSX.Element => {
  const { disabled, id, field, max, min, placeholder, type } = props;
  const { name, value, onBlur, onChange } = field;

  return (
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
  );
};
