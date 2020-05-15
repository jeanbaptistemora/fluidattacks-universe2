import _ from "lodash";
import React from "react";
import { slide as BurgerMenu } from "react-burger-menu";
import Media from "react-media";
import { useHistory } from "react-router-dom";
import { default as logo } from "../../../../resources/integrates.svg";
import { Can } from "../../../../utils/authz/Can";
import translate from "../../../../utils/translations/translate";
import { default as style } from "./index.css";

interface ISidebarProps {
  onLogoutClick(): void;
  onOpenAccessTokenModal(): void;
  onOpenAddUserModal(): void;
}

const sidebar: React.FC<ISidebarProps> = (props: ISidebarProps): JSX.Element => {
  const { onOpenAddUserModal, onOpenAccessTokenModal, onLogoutClick } = props;
  const { push } = useHistory();

  const handleLogoClick: (() => void) = (): void => { push("/home"); };

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
        <Can do="backend_api_resolvers_user__do_add_user">
          <li onClick={onOpenAddUserModal}>
            <div className={style.item}><i className="icon pe-7s-plus" />
              <span className={style.label}>{translate.t("sidebar.user")}</span>
            </div>
          </li>
        </Can>
        <li onClick={onOpenAccessTokenModal}>
          <div className={style.item}><i className="icon pe-7s-user" />
            <span className={style.label}>{translate.t("sidebar.token")}</span>
          </div>
        </li>
      </ul>
      <div className={style.bottomBar}>
        <div className={style.version}><small>integrates_version</small></div>
        <ul>
          <li onClick={onLogoutClick}><a><span className="icon pe-7s-power" /></a></li>
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
