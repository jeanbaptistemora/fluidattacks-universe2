import type { FC, ReactNode } from "react";
import React from "react";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase, useHandlers } from "../InputBase";
import { StyledSelect } from "../styles";

interface ISelectProps extends IInputBase<HTMLSelectElement> {
  children?: ReactNode;
}

type TSelectProps = ISelectProps & TFieldProps;

const FormikSelect: FC<TSelectProps> = ({
  children,
  disabled,
  field: { name, onBlur: fieldBlur, onChange: fieldChange, value },
  form,
  id,
  label,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  placeholder,
  required,
  tooltip,
  variant,
}: Readonly<TSelectProps>): JSX.Element => {
  const [handleBlur, handleChange] = useHandlers(
    { onBlur: fieldBlur, onChange: fieldChange },
    { onBlur, onChange }
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
        onChange={handleChange}
        onFocus={onFocus}
        onKeyDown={onKeyDown}
        placeholder={placeholder}
        value={value}
      >
        {children}
      </StyledSelect>
    </InputBase>
  );
};

export type { ISelectProps };
export { FormikSelect };
