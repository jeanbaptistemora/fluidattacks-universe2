import _ from "lodash";
import React from "react";
import { Props as BurgerMenuProps, slide as Menu } from "react-burger-menu";
import Media from "react-media";
import { default as logo } from "../../../../resources/integrates.png";
import translate from "../../../../utils/translations/translate";
import { TabItem } from "../TabItem";
import style from "./index.css";

interface ISidebarProps {
  onLogoutClick(): void;
}

/**
 * Necessary because current type definitions for this component are outdated.
 * @view: https://github.com/negomi/react-burger-menu/issues/65#issuecomment-446240217
 */
type UpdatedBurgerProps = BurgerMenuProps & { disableCloseOnEsc: boolean };
// tslint:disable-next-line: variable-name
const BurgerMenu: React.SFC<UpdatedBurgerProps> = (props: UpdatedBurgerProps): JSX.Element => (<Menu {...props} />);

const sidebar: React.SFC<ISidebarProps> = (props: ISidebarProps): JSX.Element => {
  const handleEsClick: (() => void) = (): void => { localStorage.setItem("lang", "es"); location.reload(); };
  const handleEnClick: (() => void) = (): void => { localStorage.setItem("lang", "en"); location.reload(); };
  const handleLogoutClick: (() => void) = (): void => { props.onLogoutClick(); };
  const handleLogoClick: (() => void) = (): void => { location.hash = "#!/home"; };
  const handleFormsClick: (() => void) = (): void => { location.hash = "#!/forms"; };
  const isAnalyst: boolean = _.includes(["admin", "analyst"], (window as Window & { userRole: string }).userRole);

  const renderAnalystTabs: (() => JSX.Element) = (): JSX.Element => (
    <React.Fragment>
      <TabItem
        icon={<i className="icon s7-note2" />}
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
          <li onClick={handleLogoutClick}><a><span className="icon s7-power" /></a></li>
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
