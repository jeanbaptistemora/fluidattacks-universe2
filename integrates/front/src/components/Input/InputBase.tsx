import type { FC, FocusEvent, KeyboardEvent, ReactNode } from "react";
import React from "react";

import type { ILabelProps } from "./Label";
import { Label } from "./Label";
import type { IStyledInputProps } from "./styles";
import { InputBox, InputWrapper } from "./styles";

import { Alert } from "components/Alert";

interface IInputBase<T = HTMLElement>
  extends IStyledInputProps,
    Omit<ILabelProps, "children" | "htmlFor"> {
  disabled?: boolean;
  id?: string;
  label?: ILabelProps["children"];
  name: string;
  onBlur?: (event: FocusEvent<T>) => void;
  onFocus?: (event: FocusEvent<T>) => void;
  onKeyDown?: (event: KeyboardEvent<T>) => void;
}

interface IInputBaseProps extends IInputBase {
  alert?: string;
  children?: ReactNode;
}

const InputBase: FC<IInputBaseProps> = ({
  alert,
  children,
  id,
  label,
  name,
  required,
  tooltip,
  variant = "solid",
}: Readonly<IInputBaseProps>): JSX.Element => (
  <InputBox showAlert={alert !== undefined}>
    {label === undefined ? undefined : (
      <Label htmlFor={id ?? name} required={required} tooltip={tooltip}>
        {label}
      </Label>
    )}
    <InputWrapper variant={variant}>{children}</InputWrapper>
    <Alert icon={true} show={alert !== undefined}>
      {alert}
    </Alert>
  </InputBox>
);

export type { IInputBase };
export { InputBase };
