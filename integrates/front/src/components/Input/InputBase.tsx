import React from "react";

import type { IStyledInputProps } from "./styles";
import { InputBox, InputWrapper } from "./styles";

import { Alert } from "components/Alert";
import { Text } from "components/Text";

interface IInputBaseProps extends Partial<IStyledInputProps> {
  alert?: string;
  children?: React.ReactNode;
  id?: string;
  label?: React.ReactNode;
  name: string;
}

const InputBase: React.FC<IInputBaseProps> = ({
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
    <Alert icon={true} variant={"error"}>
      {alert}
    </Alert>
  </InputBox>
);

export type { IInputBaseProps };
export { InputBase };
