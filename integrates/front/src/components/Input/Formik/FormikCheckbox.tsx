import { faCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC, FocusEvent } from "react";
import React, { Fragment, useCallback } from "react";
import styled from "styled-components";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase } from "../InputBase";

interface ICheckboxProps extends IInputBase<HTMLInputElement> {
  checked?: boolean;
  value: string;
}

type TCheckboxProps = ICheckboxProps & TFieldProps;

const CheckboxBox = styled.span.attrs({
  className: "",
})<Pick<ICheckboxProps, "disabled">>`
  background-color: #e9e9ed;
  border: 1px solid #c7c7d1;
  border-radius: 4px;
  color: #121216;
  display: inline-block;
  height: 18px;
  margin-right: 6px;
  position: relative;
  transition: all 0.3s ease;
  vertical-align: bottom;
  width: 18px;

  ${({ disabled = false }): string =>
    disabled
      ? `
      cursor: not-allowed;
      opacity: 0.5;
      `
      : ""}

  :hover {
    background-color: #c7c7d1;
    border-color: #a5a5b6;
  }

  > svg {
    height: 70%;
    left: 15%;
    position: absolute;
    top: 15%;
    width: 70%;
  }
`;

const CheckboxInput = styled.input.attrs({
  type: "checkbox",
})`
  display: none;

  :not(:checked) + svg {
    display: none;
  }
`;

const FormikCheckbox: FC<TCheckboxProps> = ({
  disabled,
  field: { checked, name, onBlur: fieldBlur, onChange: fieldChange, value },
  form,
  id,
  label,
  onBlur,
  required,
  tooltip,
}: Readonly<TCheckboxProps>): JSX.Element => {
  const handleBlur = useCallback(
    (ev: FocusEvent<HTMLInputElement>): void => {
      fieldBlur(ev);
      onBlur?.(ev);
    },
    [fieldBlur, onBlur]
  );

  return (
    <InputBase
      form={form}
      id={id}
      label={
        <Fragment>
          <CheckboxBox disabled={disabled}>
            <CheckboxInput
              aria-label={name}
              checked={checked}
              disabled={disabled}
              id={id}
              name={name}
              onBlur={handleBlur}
              onChange={fieldChange}
              value={value}
            />
            <FontAwesomeIcon icon={faCheck} />
          </CheckboxBox>
          {label}
        </Fragment>
      }
      name={name}
      required={required}
      tooltip={tooltip}
    />
  );
};

export type { ICheckboxProps };
export { FormikCheckbox };
