/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */
/* eslint-disable react/forbid-component-props */
import type { IconProp } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
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
  children?: ReactNode;
  icon?: IconProp;
  id?: string;
  onClick?: MouseEventHandler<HTMLButtonElement>;
  tooltip?: string;
}

const Button: FC<IButtonProps> = ({
  children,
  disabled,
  disp = "inline-block",
  icon,
  id,
  name,
  onClick,
  size,
  type,
  tooltip,
  value,
  variant,
}: Readonly<IButtonProps>): JSX.Element => {
  const Btn = (
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
      {icon === undefined ? undefined : (
        <FontAwesomeIcon
          className={children === undefined ? undefined : "mr2"}
          icon={icon}
        />
      )}
      {children}
    </StyledButton>
  );

  return id === undefined || tooltip === undefined ? (
    Btn
  ) : (
    <Tooltip disp={disp} id={`${id}-tooltip`} tip={tooltip}>
      {Btn}
    </Tooltip>
  );
};

export type { IButtonProps };
export { Button, ButtonGroup };
