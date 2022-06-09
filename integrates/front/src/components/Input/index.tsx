import React, { useCallback, useState } from "react";

import { Alert, Container, StyledInput } from "./styles";
import type { IStyledInputProps } from "./styles";

interface IInputProps extends IStyledInputProps {
  alertMsg?: string;
  validate?: (val: string) => string | undefined;
}

const Input: React.FC<IInputProps> = ({
  alertMsg = "",
  disabled = false,
  id,
  placeholder,
  type = "text",
  validate = (): undefined => undefined,
  variant = "solid",
}: Readonly<IInputProps>): JSX.Element => {
  const [alert, setAlert] = useState<string>(alertMsg);
  const handleChange = useCallback(
    (ev: React.ChangeEvent<HTMLInputElement>): void => {
      ev.preventDefault();
      setAlert(validate(ev.target.value) ?? "");
    },
    [validate]
  );

  return (
    <Container>
      <StyledInput
        disabled={disabled}
        id={id}
        onChange={handleChange}
        placeholder={placeholder}
        type={type}
        variant={variant}
      />
      <Alert show={alert.length > 0}>{alert}</Alert>
    </Container>
  );
};

export type { IInputProps };
export { Input };
