/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";
import { Link } from "react-router-dom";

import { SidebarContainer, SidebarMenu } from "./styles";

import { Logo } from "components/Logo";

const Sidebar: React.FC = (): JSX.Element => {
  return (
    <SidebarContainer>
      <SidebarMenu>
        <li>
          <Link to={"/home"}>
            <Logo height={45} width={45} />
          </Link>
        </li>
      </SidebarMenu>
    </SidebarContainer>
  );
};

export { Sidebar };
