import type { FC, FocusEvent, ReactNode } from "react";
import React, { useCallback } from "react";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase } from "../InputBase";
import { StyledSelect } from "../styles";

interface ISelectProps extends IInputBase<HTMLSelectElement> {
  children?: ReactNode;
}

type TSelectProps = ISelectProps & TFieldProps;

const FormikSelect: FC<TSelectProps> = ({
  children,
  disabled,
  field: { name, onBlur: onBlurField, onChange, value },
  form,
  id,
  label,
  onBlur,
  onFocus,
  onKeyDown,
  required,
  tooltip,
  variant,
}: Readonly<TSelectProps>): JSX.Element => {
  const handleBlur = useCallback(
    (ev: FocusEvent<HTMLSelectElement>): void => {
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
      <StyledSelect
        aria-label={name}
        autoComplete={"off"}
        disabled={disabled}
        id={id}
        name={name}
        onBlur={handleBlur}
        onChange={onChange}
        onFocus={onFocus}
        onKeyDown={onKeyDown}
        value={value}
      >
        {children}
      </StyledSelect>
    </InputBase>
  );
};

export type { ISelectProps };
export { FormikSelect };
