/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type {
  ButtonHTMLAttributes,
  FC,
  MouseEventHandler,
  ReactElement,
  ReactNode,
} from "react";
import React from "react";
import { IconContext } from "react-icons";
import type { IconType } from "react-icons";

import { StyledButton } from "./styledComponents";
import type { IStyledButtonProps } from "./types";

import { Container } from "../Container";

interface IButtonProps
  extends IStyledButtonProps,
    ButtonHTMLAttributes<HTMLButtonElement> {
  children?: ReactNode;
  icon?: ReactElement<IconType>;
  iconSide?: "left" | "right";
  onClick?: MouseEventHandler<HTMLButtonElement>;
}

const Button: FC<IButtonProps> = ({
  children,
  display,
  icon,
  iconSide = "left",
  name,
  onClick,
  size,
  type,
  variant,
}: Readonly<IButtonProps>): JSX.Element => {
  return (
    <StyledButton
      display={display}
      name={name}
      onClick={onClick}
      size={size}
      type={type}
      variant={variant}
    >
      <Container
        align={"center"}
        display={"flex"}
        justify={display === "block" ? "center" : "unset"}
      >
        {iconSide === "left" ? (
          <IconContext.Provider
            value={{ className: children === undefined ? undefined : "mr1" }}
          >
            {icon ? icon : undefined}
            {children}
          </IconContext.Provider>
        ) : (
          <IconContext.Provider
            value={{ className: children === undefined ? undefined : "ml1" }}
          >
            {children}
            {icon ? icon : undefined}
          </IconContext.Provider>
        )}
      </Container>
    </StyledButton>
  );
};

export type { IButtonProps };
export { Button };
