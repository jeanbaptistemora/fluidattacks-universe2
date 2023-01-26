import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IInputFileProps } from "../Formik/FormikFile";
import { FormikFile } from "../Formik/FormikFile";

const InputFile: FC<IInputFileProps> = ({
  accept,
  disabled,
  id,
  label,
  multiple,
  name,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  placeholder,
  required,
  tooltip,
  validate,
  variant,
}: Readonly<IInputFileProps>): JSX.Element => (
  <Field
    accept={accept}
    component={FormikFile}
    disabled={disabled}
    id={id}
    label={label}
    multiple={multiple}
    name={name}
    onBlur={onBlur}
    onChange={onChange}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    placeholder={placeholder}
    required={required}
    tooltip={tooltip}
    validate={validate}
    variant={variant}
  />
);

export { InputFile };
