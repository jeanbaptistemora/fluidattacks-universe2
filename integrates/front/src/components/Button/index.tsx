import type {
  ButtonHTMLAttributes,
  FC,
  MouseEventHandler,
  ReactNode,
} from "react";
import React from "react";

import { ButtonGroup } from "./ButtonGroup";
import type { IStyledButtonProps } from "./styles";
import { StyledButton } from "./styles";

import { Tooltip } from "components/Tooltip";

interface IButtonProps
  extends IStyledButtonProps,
    ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  id?: string;
  onClick?: MouseEventHandler<HTMLButtonElement>;
  tooltip?: string;
}

const Button: FC<IButtonProps> = ({
  children,
  disabled,
  disp = "inline-block",
  id,
  name,
  onClick,
  size,
  type,
  tooltip,
  value,
  variant,
}: Readonly<IButtonProps>): JSX.Element => (
  <Tooltip
    disp={disp}
    hide={id === undefined || tooltip === undefined}
    id={`${id ?? "btn"}-tooltip`}
    tip={tooltip}
  >
    <StyledButton
      disabled={disabled}
      disp={disp}
      id={id}
      name={name}
      onClick={onClick}
      size={size}
      type={type}
      value={value}
      variant={variant}
    >
      {children}
    </StyledButton>
  </Tooltip>
);

export type { IButtonProps };
export { Button, ButtonGroup };
