/* eslint-disable react/no-multi-comp */
import { DateTimePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import type { Dayjs } from "dayjs";
import React, { useCallback } from "react";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase, useHandlers } from "../InputBase";
import { StyledInput } from "../styles";

type IInputDateTimeProps = IInputBase<HTMLInputElement>;
type TInputDateTimeProps = IInputDateTimeProps & TFieldProps;

interface IInnerInputProps {
  inputProps?: {
    onChange?: React.InputHTMLAttributes<HTMLInputElement>["onChange"];
    placeholder?: string;
    value?: string;
  };
  InputProps?: { endAdornment?: React.ReactNode };
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  inputRef?: React.Ref<any>;
}

function renderInput({
  disabled,
  form,
  field: { name, onBlur: fieldBlur },
  id,
  label,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  required,
  tooltip,
  variant = "solid",
}: Readonly<TInputDateTimeProps>): (props: IInnerInputProps) => JSX.Element {
  return function InnerInput({
    inputProps,
    InputProps,
    inputRef,
  }: Readonly<IInnerInputProps>): JSX.Element {
    const [handleBlur, handleChange] = useHandlers(
      { onBlur: fieldBlur, onChange: inputProps?.onChange },
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
        <StyledInput
          aria-label={name}
          autoComplete={"off"}
          disabled={disabled}
          id={id}
          name={name}
          onBlur={handleBlur}
          onChange={handleChange}
          onFocus={onFocus}
          onKeyDown={onKeyDown}
          placeholder={inputProps?.placeholder}
          ref={inputRef}
          type={"text"}
          value={inputProps?.value}
        />
        <div className={"mr2"}>{InputProps?.endAdornment}</div>
      </InputBase>
    );
  };
}

const FormikDateTime: React.FC<TInputDateTimeProps> = (props): JSX.Element => {
  const {
    field: { name, onChange, value },
  } = props;

  const handleChange = useCallback(
    (dateValue: Dayjs | null): void => {
      const changeEvent = new Event("change");
      // eslint-disable-next-line fp/no-mutating-methods
      Object.defineProperty(changeEvent, "target", {
        value: { name, value: dateValue },
      });
      onChange(changeEvent);
    },
    [name, onChange]
  );

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DateTimePicker
        onChange={handleChange}
        renderInput={renderInput(props)}
        value={value}
      />
    </LocalizationProvider>
  );
};

export type { IInputDateTimeProps };
export { FormikDateTime };
