import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import type { FC, FocusEvent, MouseEvent } from "react";
import React, { useCallback, useMemo } from "react";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase } from "../InputBase";
import { StyledInput } from "../styles";
import { createEvent } from "../utils";
import { Button } from "components/Button";

interface IInputNumberProps extends IInputBase<HTMLInputElement> {
  decimalPlaces?: number;
  max?: number;
  min?: number;
  placeholder?: string;
}

type TInputNumberProps = IInputNumberProps & TFieldProps;

const FormikNumber: FC<TInputNumberProps> = ({
  decimalPlaces = 0,
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
  const decPlaces = useMemo(
    (): number => (decimalPlaces < 0 ? 0 : decimalPlaces),
    [decimalPlaces]
  );
  const handleBlur = useCallback(
    (ev: FocusEvent<HTMLInputElement>): void => {
      onBlurField(ev);
      onBlur?.(ev);
    },
    [onBlur, onBlurField]
  );

  const getCurrentValue = useCallback((): number => {
    // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
    if (value === undefined) {
      return 0;
    }

    return _.toNumber(value);
  }, [value]);

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
      const newValue = (getCurrentValue() - 10 ** -decPlaces).toFixed(
        decPlaces
      );
      changeValue(Math.max(min, Number(newValue)));
    },
    [changeValue, decPlaces, getCurrentValue, min]
  );

  const handleClickPlus = useCallback(
    (ev: MouseEvent<HTMLButtonElement>): void => {
      ev.stopPropagation();
      const newValue = (getCurrentValue() + 10 ** -decPlaces).toFixed(
        decPlaces
      );
      changeValue(Math.min(max, Number(newValue)));
    },
    [changeValue, decPlaces, getCurrentValue, max]
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
        step={"any"}
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
