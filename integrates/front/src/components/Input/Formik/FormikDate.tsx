import type { FC, FocusEvent } from "react";
import React, { useCallback } from "react";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase } from "../InputBase";
import { StyledInput } from "../styles";

interface IInputDateProps extends IInputBase<HTMLInputElement> {
  max?: Date;
  min?: Date;
}

type TInputDateProps = IInputDateProps & {
  field: TFieldProps["field"];
  form: Pick<TFieldProps["form"], "errors" | "touched">;
};

const FormikDate: FC<TInputDateProps> = ({
  disabled,
  field: { name, onBlur: onBlurField, onChange, value },
  form,
  id,
  label,
  max,
  min,
  onBlur,
  onFocus,
  onKeyDown,
  required,
  tooltip,
  variant = "solid",
}: Readonly<TInputDateProps>): JSX.Element => {
  const handleBlur = useCallback(
    (ev: FocusEvent<HTMLInputElement>): void => {
      onBlurField(ev);
      onBlur?.(ev);
    },
    [onBlur, onBlurField]
  );

  return (
    <InputBase
      form={form}
      id={id}
      label={label}
      name={name}
      required={required}
      tooltip={tooltip}
      variant={variant}
    >
      <StyledInput
        aria-label={name}
        autoComplete={"off"}
        disabled={disabled}
        id={id}
        max={max?.toISOString().substring(0, 10)}
        min={min?.toISOString().substring(0, 10)}
        name={name}
        onBlur={handleBlur}
        onChange={onChange}
        onFocus={onFocus}
        onKeyDown={onKeyDown}
        type={"date"}
        value={value}
      />
    </InputBase>
  );
};

export type { IInputDateProps };
export { FormikDate };
