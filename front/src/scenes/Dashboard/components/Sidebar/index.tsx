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
}

const sidebar: React.FC<ISidebarProps> = (props: ISidebarProps): JSX.Element => {
  const handleEsClick: (() => void) = (): void => { localStorage.setItem("lang", "es"); location.reload(); };
  const handleEnClick: (() => void) = (): void => { localStorage.setItem("lang", "en"); location.reload(); };
  const handleLogoutClick: (() => void) = (): void => { props.onLogoutClick(); };
  const handleLogoClick: (() => void) = (): void => { location.hash = "#!/home"; };
  const handleFormsClick: (() => void) = (): void => { location.hash = "#!/forms/progress"; };
  const isAnalyst: boolean = _.includes(["admin", "analyst"], (window as Window & { userRole: string }).userRole);

  const renderAnalystTabs: (() => JSX.Element) = (): JSX.Element => (
    <React.Fragment>
      <TabItem
        icon={<i className="icon pe-7s-note2" />}
        labelText={translate.t("sidebar.forms")}
        onClick={handleFormsClick}
      />
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
      <ul>
        {isAnalyst ? renderAnalystTabs() : undefined}
      </ul>
      <div className={style.bottomBar}>
        <div className={style.version}><small>integrates_version</small></div>
        <ul>
          <li onClick={handleEsClick}><a>ES</a></li>
          <li onClick={handleEnClick}><a>EN</a></li>
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
