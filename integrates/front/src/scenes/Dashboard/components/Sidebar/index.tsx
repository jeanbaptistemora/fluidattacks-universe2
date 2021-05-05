import {
  faFolderPlus,
  faKey,
  faSignOutAlt,
  faUserPlus,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React from "react";
import { slide as BurgerMenu } from "react-burger-menu";
import Media from "react-media";
import { Link } from "react-router-dom";

import { Logo, LogoutButton, MenuButton } from "./styles";

import { ConfirmDialog } from "components/ConfirmDialog";
import { TooltipWrapper } from "components/TooltipWrapper/index";
import style from "scenes/Dashboard/components/Sidebar/index.css";
import { Can } from "utils/authz/Can";
import {
  CI_COMMIT_SHA,
  CI_COMMIT_SHORT_SHA,
  INTEGRATES_DEPLOYMENT_DATE,
} from "utils/ctx";
import { translate } from "utils/translations/translate";

interface ISidebarProps {
  userEmail: string;
  userRole: string | undefined;
  onLogoutClick: () => void;
  onOpenAccessTokenModal: () => void;
  onOpenAddOrganizationModal: () => void;
  onOpenAddUserModal: () => void;
}

const sidebar: React.FC<ISidebarProps> = (
  props: ISidebarProps
): JSX.Element => {
  const {
    userEmail,
    userRole,
    onLogoutClick,
    onOpenAccessTokenModal,
    onOpenAddOrganizationModal,
    onOpenAddUserModal,
  } = props;
  const renderMenu: (isNormalScreenSize: boolean) => JSX.Element = (
    isNormalScreenSize: boolean
  ): JSX.Element => (
    <BurgerMenu
      burgerButtonClassName={style.burgerButton}
      crossButtonClassName={style.closeButton}
      disableCloseOnEsc={true}
      isOpen={isNormalScreenSize}
      menuClassName={style.container}
      noOverlay={isNormalScreenSize}
      width={210}
    >
      <ul className={style.menuList}>
        <li>
          <Link to={"/home"}>
            <Logo />
          </Link>
        </li>
        <Can do={"backend_api_mutations_add_stakeholder_mutate"}>
          <li>
            <TooltipWrapper
              id={"addUser"}
              message={translate.t("sidebar.user.tooltip")}
              placement={"right"}
            >
              <MenuButton onClick={onOpenAddUserModal}>
                <FontAwesomeIcon icon={faUserPlus} />
                {translate.t("sidebar.user.text")}
              </MenuButton>
            </TooltipWrapper>
          </li>
        </Can>
        <Can do={"backend_api_mutations_create_organization_mutate"}>
          <li>
            <TooltipWrapper
              id={"addOrg"}
              message={translate.t("sidebar.newOrganization.tooltip")}
              placement={"right"}
            >
              <MenuButton onClick={onOpenAddOrganizationModal}>
                <FontAwesomeIcon icon={faFolderPlus} />
                &nbsp;{translate.t("sidebar.newOrganization.text")}
              </MenuButton>
            </TooltipWrapper>
          </li>
        </Can>
        <li>
          <TooltipWrapper
            id={"apiToken"}
            message={translate.t("sidebar.token.tooltip")}
            placement={"right"}
          >
            <MenuButton onClick={onOpenAccessTokenModal}>
              <FontAwesomeIcon icon={faKey} />
              &nbsp;{translate.t("sidebar.token.text")}
            </MenuButton>
          </TooltipWrapper>
        </li>
      </ul>
      <div className={style.bottomBar}>
        <div className={style.version}>
          <small>{userEmail}</small>
        </div>
        {_.isUndefined(userRole) || _.isEmpty(userRole) ? undefined : (
          <div className={style.version}>
            <small>
              {translate.t("sidebar.role")}&nbsp;
              {translate.t(`userModal.roles.${_.camelCase(userRole)}`)}
            </small>
          </div>
        )}
        <div className={style.version}>
          <small>
            {translate.t("sidebar.deploymentDate")}&nbsp;
            {INTEGRATES_DEPLOYMENT_DATE}
          </small>
        </div>
        <div className={style.version}>
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
        <TooltipWrapper
          displayClass={"flex"}
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
    </BurgerMenu>
  );

  return (
    <React.StrictMode>
      <Media query={"(min-width: 768px)"}>{renderMenu}</Media>
    </React.StrictMode>
  );
};

export { sidebar as Sidebar };
