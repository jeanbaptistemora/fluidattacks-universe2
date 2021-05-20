import {
  faAngleDoubleLeft,
  faAngleDoubleRight,
  faFolderPlus,
  faUserCog,
  faUserPlus,
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

import { TooltipWrapper } from "components/TooltipWrapper/index";
import { Can } from "utils/authz/Can";
import { useStoredState } from "utils/hooks";
import { translate } from "utils/translations/translate";

interface ISidebarProps {
  isLoading: boolean;
  onOpenAddOrganizationModal: () => void;
  onOpenAddUserModal: () => void;
  onOpenConfig: () => void;
}

const Sidebar: React.FC<ISidebarProps> = ({
  isLoading,
  onOpenAddOrganizationModal,
  onOpenAddUserModal,
  onOpenConfig,
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
        <Can do={"api_mutations_add_stakeholder_mutate"}>
          <li>
            <TooltipWrapper
              id={"addUser"}
              message={translate.t("sidebar.user.tooltip")}
              placement={"right"}
            >
              <SidebarButton onClick={onOpenAddUserModal}>
                <FontAwesomeIcon icon={faUserPlus} />
                {translate.t("sidebar.user.text")}
              </SidebarButton>
            </TooltipWrapper>
          </li>
        </Can>
        <Can do={"api_mutations_create_organization_mutate"}>
          <li>
            <TooltipWrapper
              id={"addOrg"}
              message={translate.t("sidebar.newOrganization.tooltip")}
              placement={"right"}
            >
              <SidebarButton onClick={onOpenAddOrganizationModal}>
                <FontAwesomeIcon icon={faFolderPlus} />
                &nbsp;{translate.t("sidebar.newOrganization.text")}
              </SidebarButton>
            </TooltipWrapper>
          </li>
        </Can>
        <li>
          <TooltipWrapper
            id={"globalConfig"}
            message={translate.t("sidebar.configuration.tooltip")}
            placement={"right"}
          >
            <SidebarButton onClick={onOpenConfig}>
              <FontAwesomeIcon icon={faUserCog} />
              &nbsp;{translate.t("sidebar.configuration.text")}
            </SidebarButton>
          </TooltipWrapper>
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
