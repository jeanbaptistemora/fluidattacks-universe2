import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon as Icon } from "@fortawesome/react-fontawesome";
import type { FC, FocusEvent, KeyboardEvent, ReactNode } from "react";
import React from "react";

import type { IStyledInputProps } from "./styles";
import { InputBox, InputWrapper } from "./styles";

import { Alert } from "components/Alert";
import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";

interface IInputBase<T = HTMLElement> extends Partial<IStyledInputProps> {
  disabled?: boolean;
  id?: string;
  label?: ReactNode;
  name: string;
  onBlur?: (event: FocusEvent<T>) => void;
  onFocus?: (event: FocusEvent<T>) => void;
  onKeyDown?: (event: KeyboardEvent<T>) => void;
  tooltip?: string;
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
  tooltip,
  variant = "solid",
}: Readonly<IInputBaseProps>): JSX.Element => (
  <InputBox showAlert={alert !== undefined}>
    {label === undefined ? undefined : (
      <label htmlFor={id}>
        <Text disp={"inline-block"} mb={1} mr={1}>
          {label}
        </Text>
        {tooltip === undefined ? undefined : (
          <Tooltip
            disp={"inline-block"}
            id={`${name}-tooltip`}
            place={"top"}
            tip={tooltip}
          >
            <Icon color={"#b0b0bf"} icon={faCircleInfo} size={"sm"} />
          </Tooltip>
        )}
      </label>
    )}
    <InputWrapper variant={variant}>{children}</InputWrapper>
    <Alert icon={true} show={alert !== undefined}>
      {alert}
    </Alert>
  </InputBox>
);

export type { IInputBase };
export { InputBase };
