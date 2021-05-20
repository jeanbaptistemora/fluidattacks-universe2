import {
  faAngleDoubleLeft,
  faAngleDoubleRight,
  faFolderPlus,
  faUserCog,
  faUserPlus,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
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
import { translate } from "utils/translations/translate";

interface ISidebarProps {
  collapsed: boolean;
  isLoading: boolean;
  onOpenAddOrganizationModal: () => void;
  onOpenAddUserModal: () => void;
  onOpenConfig: () => void;
  onToggle: () => void;
}

const Sidebar: React.FC<ISidebarProps> = (
  props: ISidebarProps
): JSX.Element => {
  const {
    collapsed,
    isLoading,
    onOpenAddOrganizationModal,
    onOpenAddUserModal,
    onOpenConfig,
    onToggle,
  } = props;

  return (
    <SidebarContainer collapsed={collapsed}>
      <SidebarMenu>
        <li>
          <SidebarButton onClick={onToggle}>
            <FontAwesomeIcon
              icon={collapsed ? faAngleDoubleRight : faAngleDoubleLeft}
            />
          </SidebarButton>
        </li>
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
    </SidebarContainer>
  );
};

export { Sidebar };
