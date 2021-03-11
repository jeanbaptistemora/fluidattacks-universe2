import { Badge } from "components/Badge";
import { slide as BurgerMenu } from "react-burger-menu";
import { Can } from "utils/authz/Can";
import Media from "react-media";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper/index";
import _ from "lodash";
import logo from "resources/integrates_sidebar.svg";
import style from "scenes/Dashboard/components/Sidebar/index.css";
import { translate } from "utils/translations/translate";
import { useHistory } from "react-router-dom";

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
  // eslint-disable-next-line react-hooks/rules-of-hooks
  const { push } = useHistory();
  // eslint-disable-next-line react-hooks/rules-of-hooks
  const handleLogoClick: () => void = React.useCallback((): void => {
    push("/home");
  }, [push]);

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
      {/* eslint-disable-next-line jsx-a11y/click-events-have-key-events, jsx-a11y/no-noninteractive-element-interactions */}
      <img
        alt={"integrates-logo"}
        className={style.logo}
        onClick={handleLogoClick}
        src={logo}
      />
      <ul className={style.menuList}>
        <Can do={"backend_api_mutations_add_stakeholder_mutate"}>
          {/* eslint-disable-next-line jsx-a11y/click-events-have-key-events, jsx-a11y/no-noninteractive-element-interactions */}
          <li onClick={onOpenAddUserModal}>
            <TooltipWrapper
              id={"addUser"}
              message={translate.t("sidebar.user.tooltip")}
              placement={"right"}
            >
              <div className={style.item}>
                <i className={"icon pe-7s-plus"} />
                <span className={style.label}>
                  {translate.t("sidebar.user.text")}
                </span>
              </div>
            </TooltipWrapper>
          </li>
        </Can>
        <Can do={"backend_api_mutations_create_organization_mutate"}>
          {/* eslint-disable-next-line jsx-a11y/click-events-have-key-events, jsx-a11y/no-noninteractive-element-interactions */}
          <li onClick={onOpenAddOrganizationModal}>
            <TooltipWrapper
              id={"addOrg"}
              message={translate.t("sidebar.newOrganization.tooltip")}
              placement={"right"}
            >
              <div className={style.item}>
                <i className={"icon pe-7s-plus"} />
                <span className={style.label}>
                  {translate.t("sidebar.newOrganization.text")}
                </span>
              </div>
            </TooltipWrapper>
          </li>
        </Can>
        {/* eslint-disable-next-line jsx-a11y/click-events-have-key-events, jsx-a11y/no-noninteractive-element-interactions */}
        <li onClick={onOpenAccessTokenModal}>
          <TooltipWrapper
            id={"apiToken"}
            message={translate.t("sidebar.token.tooltip")}
            placement={"right"}
          >
            <div className={style.item}>
              <i className={"icon pe-7s-user"} />
              <span className={style.label}>
                {translate.t("sidebar.token.text")}
              </span>
              <Badge>{"pro"}</Badge>
            </div>
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
              {translate.t(`userModal.roles.${userRole}`)}
            </small>
          </div>
        )}
        <div className={style.version}>
          <small>
            {translate.t("sidebar.deploymentDate")}&nbsp;
            {process.env.INTEGRATES_DEPLOYMENT_DATE}
          </small>
        </div>
        <div className={style.version}>
          <small>
            {translate.t("sidebar.commit")}&nbsp;
            <a
              // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
              href={`https://gitlab.com/fluidattacks/product/-/tree/${process.env.CI_COMMIT_SHA}`}
              rel={"noopener noreferrer"}
              target={"_blank"}
            >
              {process.env.CI_COMMIT_SHORT_SHA}
            </a>
          </small>
        </div>
        <TooltipWrapper
          displayClass={"flex"}
          id={"logOut"}
          message={"Log out of Integrates"}
          placement={"right"}
        >
          <ul className={"mt0"}>
            {/* eslint-disable-next-line jsx-a11y/click-events-have-key-events, jsx-a11y/no-noninteractive-element-interactions */}
            <li onClick={onLogoutClick}>
              {/* eslint-disable-next-line jsx-a11y/anchor-is-valid */}
              <a>
                <span className={"icon pe-7s-power"} />
              </a>
            </li>
          </ul>
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
