import { faCircleXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useState } from "react";

import type { IAlertProps, IStyledInputProps } from "./styles";
import { Alert, Container, StyledInput } from "./styles";

interface IInputProps extends IStyledInputProps {
  alertMsg?: string;
  alertType?: IAlertProps["variant"];
  validate?: (val: string) => string | undefined;
}

const Input: React.FC<IInputProps> = ({
  alertMsg = "",
  alertType = "low",
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
      <Alert show={alert.length > 0} variant={alertType}>
        <FontAwesomeIcon icon={faCircleXmark} />
        &nbsp;
        {alert}
      </Alert>
    </Container>
  );
};

export type { IInputProps };
export { Input };
