import {
  faAngleDoubleLeft,
  faAngleDoubleRight,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback } from "react";
import { Link } from "react-router-dom";

import {
  Logo,
  Preloader,
  SidebarButton,
  SidebarContainer,
  SidebarMenu,
} from "./styles";

import { useStoredState } from "utils/hooks";

interface ISidebarProps {
  isLoading: boolean;
}

const Sidebar: React.FC<ISidebarProps> = ({
  isLoading,
}: ISidebarProps): JSX.Element => {
  const [collapsed, setCollapsed] = useStoredState(
    "sidebarCollapsed",
    true,
    localStorage
  );
  const toggleSidebar = useCallback((): void => {
    setCollapsed((currentValue): boolean => !currentValue);
  }, [setCollapsed]);

  return (
    <SidebarContainer collapsed={collapsed}>
      <SidebarMenu>
        <li>
          <Link to={"/home"}>
            <Logo />
          </Link>
        </li>
      </SidebarMenu>
      {isLoading ? <Preloader /> : undefined}
      <SidebarButton onClick={toggleSidebar}>
        <FontAwesomeIcon
          icon={collapsed ? faAngleDoubleRight : faAngleDoubleLeft}
        />
      </SidebarButton>
    </SidebarContainer>
  );
};

export { Sidebar };
