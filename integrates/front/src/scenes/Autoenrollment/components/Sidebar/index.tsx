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
