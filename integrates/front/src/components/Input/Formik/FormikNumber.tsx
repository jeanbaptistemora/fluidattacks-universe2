import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC, FocusEvent, MouseEvent } from "react";
import React, { useCallback } from "react";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase } from "../InputBase";
import { StyledInput } from "../styles";
import { createEvent } from "../utils";
import { Button } from "components/Button";

interface IInputNumberProps extends IInputBase<HTMLInputElement> {
  max?: number;
  min?: number;
  placeholder?: string;
}

type TInputNumberProps = IInputNumberProps & TFieldProps;

const FormikNumber: FC<TInputNumberProps> = ({
  disabled = false,
  field: { name, onBlur: onBlurField, onChange, value },
  form,
  id,
  label,
  max = 10,
  min = 0,
  onBlur,
  onFocus,
  onKeyDown,
  placeholder,
  required,
  tooltip,
  variant = "solid",
}: Readonly<TInputNumberProps>): JSX.Element => {
  const handleBlur = useCallback(
    (ev: FocusEvent<HTMLInputElement>): void => {
      onBlurField(ev);
      onBlur?.(ev);
    },
    [onBlur, onBlurField]
  );

  const changeValue = useCallback(
    (targetValue: number): void => {
      const changeEvent = createEvent("change", name, String(targetValue));

      onChange(changeEvent);
    },
    [name, onChange]
  );

  const handleClickMinus = useCallback(
    (ev: MouseEvent<HTMLButtonElement>): void => {
      ev.stopPropagation();
      changeValue(Math.max(min, Number(value) - 1));
    },
    [changeValue, min, value]
  );

  const handleClickPlus = useCallback(
    (ev: MouseEvent<HTMLButtonElement>): void => {
      ev.stopPropagation();
      changeValue(Math.min(max, Number(value) + 1));
    },
    [changeValue, max, value]
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
        max={max}
        min={min}
        name={name}
        onBlur={handleBlur}
        onChange={onChange}
        onFocus={onFocus}
        onKeyDown={onKeyDown}
        placeholder={placeholder}
        type={"number"}
        value={value}
      />
      <Button onClick={handleClickMinus} size={"sm"}>
        <FontAwesomeIcon icon={faMinus} />
      </Button>
      <Button onClick={handleClickPlus} size={"sm"}>
        <FontAwesomeIcon icon={faPlus} />
      </Button>
    </InputBase>
  );
};

export type { IInputNumberProps };
export { FormikNumber };
