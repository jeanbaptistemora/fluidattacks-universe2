import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FieldProps } from "formik";
import type {
  ChangeEvent,
  FC,
  FocusEvent,
  MouseEvent,
  MutableRefObject,
} from "react";
import React, { useCallback, useRef } from "react";

import type { IInputBase } from "../InputBase";
import { InputBase } from "../InputBase";
import { StyledInput } from "../styles";
import { Button } from "components/Button";

interface IInputNumberProps extends IInputBase<HTMLInputElement> {
  max?: number;
  min?: number;
  placeholder?: string;
}

type TInputNumberProps = FieldProps<string, Record<string, string>> &
  IInputNumberProps;

const FormikNumber: FC<TInputNumberProps> = ({
  disabled,
  field,
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
  const { name, onBlur: onBlurField, value } = field;
  const alert = form.errors[name];

  const ref: MutableRefObject<HTMLInputElement | null> = useRef(null);
  const { setFieldValue } = form;

  const getValue = useCallback(
    (val: string = value): number => (val.length === 0 ? 0 : parseInt(val, 10)),
    [value]
  );

  const changeValue = useCallback(
    (val: number): void => {
      const newVal = Math.min(Math.max(val, min), max).toString();
      if (newVal !== value) {
        setFieldValue(name, newVal);
      }
      ref.current?.focus();
    },
    [max, min, name, setFieldValue, value]
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
      setFieldValue(name, ev.target.value);
    },
    [name, setFieldValue]
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
      alert={alert}
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
