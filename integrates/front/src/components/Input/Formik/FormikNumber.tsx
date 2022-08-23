import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type {
  ChangeEvent,
  FC,
  FocusEvent,
  MouseEvent,
  MutableRefObject,
} from "react";
import React, { useCallback, useRef, useState } from "react";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase } from "../InputBase";
import { StyledInput } from "../styles";
import { Button } from "components/Button";

interface IInputNumberProps extends IInputBase<HTMLInputElement> {
  initValue?: number;
  max?: number;
  min?: number;
  placeholder?: string;
}

type TInputNumberProps = IInputNumberProps & {
  field: TFieldProps["field"];
  form: Pick<TFieldProps["form"], "errors" | "touched">;
};

const FormikNumber: FC<TInputNumberProps> = ({
  disabled,
  field: { name, onBlur: onBlurField },
  form,
  id,
  initValue,
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
  const ref: MutableRefObject<HTMLInputElement | null> = useRef(null);
  const [value, setValue] = useState((initValue ?? "").toString());

  const getValue = useCallback(
    (val: string = value): number => (val.length === 0 ? 0 : parseInt(val, 10)),
    [value]
  );

  const changeValue = useCallback(
    (val: number): void => {
      const newVal = Math.min(Math.max(val, min), max).toString();
      if (newVal !== value) {
        setValue(newVal);
      }
      ref.current?.focus();
    },
    [max, min, value]
  );

  const handleBlur = useCallback(
    (ev: FocusEvent<HTMLInputElement>): void => {
      onBlurField(ev);
      onBlur?.(ev);
    },
    [onBlur, onBlurField]
  );

  const handleChange = useCallback(
    (ev: ChangeEvent<HTMLInputElement>): void => {
      setValue(ev.target.value);
    },
    [setValue]
  );

  const handleClickMinus = useCallback(
    (ev: MouseEvent<HTMLButtonElement>): void => {
      ev.stopPropagation();
      changeValue(getValue() - 1);
    },
    [changeValue, getValue]
  );

  const handleClickPlus = useCallback(
    (ev: MouseEvent<HTMLButtonElement>): void => {
      ev.stopPropagation();
      changeValue(getValue() + 1);
    },
    [changeValue, getValue]
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
        onChange={handleChange}
        onFocus={onFocus}
        onKeyDown={onKeyDown}
        placeholder={placeholder}
        ref={ref}
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
