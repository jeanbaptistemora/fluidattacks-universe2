import { FieldArray } from "formik";
import type { FC, ReactNode } from "react";
import React from "react";

import { ActionButtons } from "./actionButtons";
import type { IInputProps } from "./FormikInput";

interface IInputArrayProps
  extends Omit<IInputProps, "childLeft" | "childRight" | "type"> {
  initValue?: string;
  max?: number;
}

const FormikArray: FC<IInputArrayProps> = ({
  disabled,
  id,
  initValue = "",
  label,
  max = 10,
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
}: Readonly<IInputArrayProps>): JSX.Element => {
  return (
    <FieldArray name={name}>
      {({ form, push, remove }): ReactNode => {
        return (
          <ActionButtons
            disabled={disabled}
            form={form}
            id={id}
            initValue={initValue}
            label={label}
            max={max}
            name={name}
            onBlur={onBlur}
            onChange={onChange}
            onFocus={onFocus}
            onKeyDown={onKeyDown}
            placeholder={placeholder}
            push={push}
            remove={remove}
            required={required}
            tooltip={tooltip}
            validate={validate}
            variant={variant}
          />
        );
      }}
    </FieldArray>
  );
};

export type { IInputArrayProps };
export { FormikArray };
