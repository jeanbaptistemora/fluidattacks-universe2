/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { FC, ReactNode } from "react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { SideBarBox } from "./styles";
import { SideBarTab } from "./Tab";

interface ISideBarProps {
  children: ReactNode;
  initial?: string;
}

const SideBar: FC<ISideBarProps> = ({
  children,
  initial = "/",
}: Readonly<ISideBarProps>): JSX.Element => (
  <MemoryRouter initialEntries={[initial]}>
    <SideBarBox>{children}</SideBarBox>
  </MemoryRouter>
);

export type { ISideBarProps };
export { SideBar, SideBarTab };
