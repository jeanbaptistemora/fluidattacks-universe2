/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable react/forbid-component-props */

import type { IconProp } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC } from "react";
import React from "react";
import type { NavLinkProps } from "react-router-dom";
import { NavLink } from "react-router-dom";
import styled from "styled-components";

interface ISideBarTabProps extends Pick<NavLinkProps, "children" | "to"> {
  disabled?: boolean;
  icon?: IconProp;
}

const SideBarLink = styled(NavLink).attrs({
  className: "SideBarTab",
})`
  border-left: 4px solid transparent;
  color: #c7c7d1;
  display: block;
  padding: 10px 20px;
  position: relative;
  transition: all 0.3s;

  &[aria-disabled="true"] {
    opacity: 0.5;
  }

  :not([aria-disabled="true"]) {
    :hover {
      color: #e9e9ed;
    }
  }

  &.active {
    border-left-color: #f2182a;
    color: #e9e9ed;
  }

  ::after {
    border-bottom: 1px solid #65657b;
    bottom: 0;
    content: "";
    left: 20px;
    position: absolute;
    width: calc(100% - 40px);
  }
`;

const SideBarTab: FC<ISideBarTabProps> = ({
  children,
  disabled,
  icon,
  to,
}: Readonly<ISideBarTabProps>): JSX.Element => (
  <SideBarLink aria-disabled={disabled} to={to}>
    {icon === undefined ? undefined : (
      <FontAwesomeIcon
        className={children === undefined ? undefined : "mr2"}
        icon={icon}
      />
    )}
    {children}
  </SideBarLink>
);

export type { ISideBarTabProps };
export { SideBarTab };
