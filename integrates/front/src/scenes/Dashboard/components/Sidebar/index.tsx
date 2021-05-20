import {
  faAngleDoubleLeft,
  faAngleDoubleRight,
  faFolderPlus,
  faSignOutAlt,
  faUserCog,
  faUserPlus,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { Link } from "react-router-dom";

import {
  ExtraInfo,
  Logo,
  LogoutButton,
  Preloader,
  SidebarButton,
  SidebarContainer,
  SidebarMenu,
} from "./styles";

import { ConfirmDialog } from "components/ConfirmDialog";
import { TooltipWrapper } from "components/TooltipWrapper/index";
import { Can } from "utils/authz/Can";
import {
  CI_COMMIT_SHA,
  CI_COMMIT_SHORT_SHA,
  INTEGRATES_DEPLOYMENT_DATE,
} from "utils/ctx";
import { translate } from "utils/translations/translate";

interface ISidebarProps {
  collapsed: boolean;
  isLoading: boolean;
  onLogoutClick: () => void;
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
    onLogoutClick,
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
      {collapsed ? undefined : (
        <ExtraInfo>
          <div>
            <small>
              {translate.t("sidebar.deploymentDate")}&nbsp;
              {INTEGRATES_DEPLOYMENT_DATE}
            </small>
          </div>
          <div>
            <small>
              {translate.t("sidebar.commit")}&nbsp;
              <a
                href={`https://gitlab.com/fluidattacks/product/-/tree/${CI_COMMIT_SHA}`}
                rel={"noopener noreferrer"}
                target={"_blank"}
              >
                {CI_COMMIT_SHORT_SHA}
              </a>
            </small>
          </div>
        </ExtraInfo>
      )}
      <div>
        <TooltipWrapper
          id={"logOut"}
          message={"Log out of Integrates"}
          placement={"right"}
        >
          <ConfirmDialog title={"Logout"}>
            {(confirm): React.ReactNode => {
              function handleLogoutClick(): void {
                confirm(onLogoutClick);
              }

              return (
                <LogoutButton onClick={handleLogoutClick}>
                  <FontAwesomeIcon icon={faSignOutAlt} />
                </LogoutButton>
              );
            }}
          </ConfirmDialog>
        </TooltipWrapper>
      </div>
    </SidebarContainer>
  );
};

export { Sidebar };
