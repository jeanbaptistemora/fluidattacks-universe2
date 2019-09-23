import _ from "lodash";
import React from "react";
import { slide as BurgerMenu } from "react-burger-menu";
import Media from "react-media";
import { default as logo } from "../../../../resources/integrates.png";
import translate from "../../../../utils/translations/translate";
import { TabItem } from "../TabItem";
import style from "./index.css";

interface ISidebarProps {
  onLogoutClick(): void;
  onOpenAccessTokenModal(): void;
}

const sidebar: React.FC<ISidebarProps> = (props: ISidebarProps): JSX.Element => {
  const handleOpenUpdateTokenModal: (() => void) = (): void => { props.onOpenAccessTokenModal(); };
  const handleLogoutClick: (() => void) = (): void => { props.onLogoutClick(); };
  const handleLogoClick: (() => void) = (): void => { location.hash = "#!/home"; };
  const isAnalyst: boolean = _.includes(["admin", "analyst"], (window as Window & { userRole: string }).userRole);

  const renderAnalystTabs: (() => JSX.Element) = (): JSX.Element => (
    <React.Fragment>
      <TabItem icon={<i className="icon pe-7s-note2" />} label={translate.t("sidebar.forms")} to="/forms" />
      <React.StrictMode>
        <li onClick={handleOpenUpdateTokenModal}>
          <div className={style.item}><i className="icon pe-7s-user" />
            <span className={style.label}>{translate.t("sidebar.token")}</span>
          </div>
        </li>
      </React.StrictMode>
    </React.Fragment>);

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
        {isAnalyst ? renderAnalystTabs() : undefined}
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
