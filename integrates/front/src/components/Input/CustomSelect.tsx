import type { FieldProps } from "formik";
import type { FC, FocusEvent, KeyboardEvent, ReactNode } from "react";
import React, { useCallback } from "react";

import type { IInputBase } from "./InputBase";
import { InputBase } from "./InputBase";
import { StyledSelect } from "./styles";

interface ISelectProps extends IInputBase {
  children?: ReactNode;
  onBlur?: (event: FocusEvent<HTMLSelectElement>) => void;
  onFocus?: (event: FocusEvent<HTMLSelectElement>) => void;
  onKeyDown?: (event: KeyboardEvent<HTMLSelectElement>) => void;
}

type TSelectProps = FieldProps<string, Record<string, string>> & ISelectProps;

const CustomSelect: FC<TSelectProps> = ({
  children,
  disabled,
  field,
  form,
  id,
  label,
  onBlur,
  onFocus,
  onKeyDown,
  variant,
}: Readonly<TSelectProps>): JSX.Element => {
  const { name, onBlur: onBlurField, onChange, value } = field;
  const alert = form.errors[name];

  const handleBlur = useCallback(
    (ev: FocusEvent<HTMLSelectElement>): void => {
      onBlurField(ev);
      onBlur?.(ev);
    },
    [onBlur, onBlurField]
  );

  return (
    <InputBase
      alert={alert}
      id={id}
      label={label}
      name={name}
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
export { CustomSelect };
