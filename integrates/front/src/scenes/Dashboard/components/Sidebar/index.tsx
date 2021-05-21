import {
  faAngleDoubleLeft,
  faAngleDoubleRight,
  faFolderPlus,
  faUserPlus,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import {
  Logo,
  Preloader,
  SidebarButton,
  SidebarContainer,
  SidebarMenu,
} from "./styles";

import { TooltipWrapper } from "components/TooltipWrapper/index";
import { Can } from "utils/authz/Can";
import { useStoredState } from "utils/hooks";

interface ISidebarProps {
  isLoading: boolean;
  onOpenAddOrganizationModal: () => void;
  onOpenAddUserModal: () => void;
}

const Sidebar: React.FC<ISidebarProps> = ({
  isLoading,
  onOpenAddOrganizationModal,
  onOpenAddUserModal,
}: ISidebarProps): JSX.Element => {
  const { t } = useTranslation();

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
        <Can do={"api_mutations_add_stakeholder_mutate"}>
          <li>
            <TooltipWrapper
              id={"addUser"}
              message={t("sidebar.user.tooltip")}
              placement={"right"}
            >
              <SidebarButton onClick={onOpenAddUserModal}>
                <FontAwesomeIcon icon={faUserPlus} />
                {t("sidebar.user.text")}
              </SidebarButton>
            </TooltipWrapper>
          </li>
        </Can>
        <Can do={"api_mutations_create_organization_mutate"}>
          <li>
            <TooltipWrapper
              id={"addOrg"}
              message={t("sidebar.newOrganization.tooltip")}
              placement={"right"}
            >
              <SidebarButton onClick={onOpenAddOrganizationModal}>
                <FontAwesomeIcon icon={faFolderPlus} />
                &nbsp;{t("sidebar.newOrganization.text")}
              </SidebarButton>
            </TooltipWrapper>
          </li>
        </Can>
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
