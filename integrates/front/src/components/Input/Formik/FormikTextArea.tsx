import React from "react";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase, useHandlers } from "../InputBase";
import { StyledTextArea } from "../styles";

interface ITextAreaProps extends IInputBase<HTMLTextAreaElement> {
  placeholder?: string;
  rows?: number;
}

type TTextAreaProps = ITextAreaProps & TFieldProps;

const FormikTextArea: React.FC<TTextAreaProps> = ({
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
  rows = 3,
  tooltip,
  variant,
}: Readonly<TTextAreaProps>): JSX.Element => {
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
      <StyledTextArea
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
        rows={rows}
        value={value}
      />
    </InputBase>
  );
};

export type { ITextAreaProps };
export { FormikTextArea };
