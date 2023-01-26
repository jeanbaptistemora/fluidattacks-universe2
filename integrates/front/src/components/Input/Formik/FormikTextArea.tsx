import React from "react";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase, useHandlers } from "../InputBase";
import { StyledTextArea } from "../styles";
import { Tag } from "components/Tag";

interface ITextAreaProps extends IInputBase<HTMLTextAreaElement> {
  count?: boolean;
  placeholder?: string;
  rows?: number;
}

type TTextAreaProps = ITextAreaProps & TFieldProps;

const FormikTextArea: React.FC<TTextAreaProps> = ({
  count = false,
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
  variant = "solid",
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
      {count ? (
        <div className={"self-end"}>
          <Tag variant={"gray"}>{value.length}</Tag>
        </div>
      ) : undefined}
    </InputBase>
  );
};

export type { ITextAreaProps };
export { FormikTextArea };
