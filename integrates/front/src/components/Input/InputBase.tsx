import type { FC, FocusEvent, KeyboardEvent, ReactNode } from "react";
import React from "react";

import type { IStyledInputProps } from "./styles";
import { InputBox, InputWrapper } from "./styles";

import { Alert } from "components/Alert";
import { Text } from "components/Text";

interface IInputBase<T = HTMLElement> extends Partial<IStyledInputProps> {
  disabled?: boolean;
  id?: string;
  label?: ReactNode;
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
  variant = "solid",
}: Readonly<IInputBaseProps>): JSX.Element => (
  <InputBox showAlert={alert !== undefined}>
    {label === undefined ? undefined : (
      <label htmlFor={id}>
        <Text mb={1}>{label}</Text>
      </label>
    )}
    <InputWrapper variant={variant}>{children}</InputWrapper>
    <Alert icon={true} show={alert !== undefined} variant={"error"}>
      {alert}
    </Alert>
  </InputBox>
);

export type { IInputBase };
export { InputBase };
