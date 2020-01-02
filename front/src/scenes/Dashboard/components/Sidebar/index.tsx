import _ from "lodash";
import React from "react";
import { slide as BurgerMenu } from "react-burger-menu";
import Media from "react-media";
import { default as logo } from "../../../../resources/integrates.png";
import translate from "../../../../utils/translations/translate";
import { default as style } from "./index.css";

interface ISidebarProps {
  onLogoutClick(): void;
  onOpenAccessTokenModal(): void;
  onOpenAddUserModal(): void;
}

const sidebar: React.FC<ISidebarProps> = (props: ISidebarProps): JSX.Element => {
  const handleOpenAddUserModal: (() => void) = (): void => { props.onOpenAddUserModal(); };
  const handleOpenUpdateTokenModal: (() => void) = (): void => { props.onOpenAccessTokenModal(); };
  const handleLogoutClick: (() => void) = (): void => { props.onLogoutClick(); };
  const handleLogoClick: (() => void) = (): void => { location.hash = "#!/home"; };
  const isAdmin: boolean = _.includes(["admin"], (window as typeof window & { userRole: string }).userRole);
  const renderAdminTabs: (() => JSX.Element) = (): JSX.Element => (
    <React.Fragment>
      <React.StrictMode>
      <li onClick={handleOpenAddUserModal}>
          <div className={style.item}><i className="icon pe-7s-plus" />
            <span className={style.label}>{translate.t("sidebar.user")}</span>
          </div>
        </li>
      </React.StrictMode>
    </React.Fragment>
  );

  const renderMenu: ((isNormalScreenSize: boolean) => JSX.Element) = (isNormalScreenSize: boolean): JSX.Element => (
    <BurgerMenu
      burgerButtonClassName={style.burgerButton}
      crossButtonClassName={style.closeButton}
      disableCloseOnEsc={true}
      isOpen={isNormalScreenSize}
      menuClassName={style.container}
      noOverlay={isNormalScreenSize}
      width={210}
    >
      <img className={style.logo} src={logo} alt="integrates-logo" onClick={handleLogoClick} />
      <ul className={style.menuList}>
        {isAdmin ? renderAdminTabs() : undefined}
        <li onClick={handleOpenUpdateTokenModal}>
          <div className={style.item}><i className="icon pe-7s-user" />
            <span className={style.label}>{translate.t("sidebar.token")}</span>
          </div>
        </li>
      </ul>
      <div className={style.bottomBar}>
        <div className={style.version}><small>integrates_version</small></div>
        <ul>
          <li onClick={handleLogoutClick}><a><span className="icon pe-7s-power" /></a></li>
        </ul>
      </div>
    </BurgerMenu>
  );

  return (
    <React.StrictMode>
      <Media query="(min-width: 768px)">
        {renderMenu}
      </Media>
    </React.StrictMode>
  );
};

export { sidebar as Sidebar };
