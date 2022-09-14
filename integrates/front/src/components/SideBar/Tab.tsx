/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable react/forbid-component-props */

import type { IconProp } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC, ReactNode } from "react";
import React, { Fragment } from "react";
import type { NavLinkProps } from "react-router-dom";
import { NavLink } from "react-router-dom";
import styled from "styled-components";

import { SideBarHr } from "./styles";

interface ISideBarTabProps extends Pick<NavLinkProps, "children" | "to"> {
  icon?: IconProp;
  subTabs?: ReactNode[];
}

const SideBarLink = styled(NavLink).attrs({
  className: "SideBarTab",
})`
  border-left: 4px solid transparent;
  color: #c7c7d1;
  display: block;
  padding: 10px 20px;
  transition: all 0.3s;

  :hover {
    color: #e9e9ed;
  }

  &.active {
    border-color: #f2182a;
    color: #e9e9ed;
  }
`;

const SideBarTab: FC<ISideBarTabProps> = ({
  children,
  icon,
  subTabs,
  to,
}: Readonly<ISideBarTabProps>): JSX.Element => (
  <Fragment>
    <SideBarLink to={to}>
      {icon === undefined ? undefined : (
        <FontAwesomeIcon
          className={children === undefined ? undefined : "mr2"}
          icon={icon}
        />
      )}
      {children}
    </SideBarLink>
    {subTabs === undefined ? undefined : (
      <div>
        <SideBarHr />
        {subTabs}
      </div>
    )}
    <SideBarHr />
  </Fragment>
);

export type { ISideBarTabProps };
export { SideBarTab };
