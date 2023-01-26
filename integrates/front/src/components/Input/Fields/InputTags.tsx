import { Field } from "formik";
import React from "react";

import type { IInputTagsProps } from "../Formik/FormikTags";
import { FormikTags } from "../Formik/FormikTags";

const InputTags: React.FC<IInputTagsProps> = ({
  disabled,
  id,
  label,
  name,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  onRemove,
  placeholder,
  required,
  tooltip,
  validate,
  variant,
}): JSX.Element => (
  <Field
    component={FormikTags}
    disabled={disabled}
    id={id}
    label={label}
    name={name}
    onBlur={onBlur}
    onChange={onChange}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    onRemove={onRemove}
    placeholder={placeholder}
    required={required}
    tooltip={tooltip}
    validate={validate}
    variant={variant}
  />
);

export { InputTags };
