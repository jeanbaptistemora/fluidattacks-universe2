import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IDatePickerProps } from "./FormikDatePicker";
import { FormikDatePicker } from "./FormikDatePicker";

const DatePicker: FC<IDatePickerProps> = ({
  disabled = false,
  id,
  label,
  max,
  min,
  name,
  onBlur,
  onFocus,
  onKeyDown,
  variant = "solid",
}: Readonly<IDatePickerProps>): JSX.Element => (
  <Field
    component={FormikDatePicker}
    disabled={disabled}
    id={id}
    label={label}
    max={max}
    min={min}
    name={name}
    onBlur={onBlur}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    variant={variant}
  />
);

export type { IDatePickerProps };
export { DatePicker };
