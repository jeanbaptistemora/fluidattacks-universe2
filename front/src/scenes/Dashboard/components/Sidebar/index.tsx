import React from "react";
import { default as logo } from "../../../../resources/integrates.png";
import { TabItem } from "../TabItem";
import style from "./index.css";

interface ISidebarProps {
  onLogoutClick(): void;
}

const sidebar: React.SFC<ISidebarProps> = (props: ISidebarProps): JSX.Element => {
  const handleEsClick: (() => void) = (): void => { localStorage.setItem("lang", "es"); location.reload(); };
  const handleEnClick: (() => void) = (): void => { localStorage.setItem("lang", "en"); location.reload(); };
  const handleLogoutClick: (() => void) = (): void => { props.onLogoutClick(); };
  const handleLogoClick: (() => void) = (): void => { location.hash = "#!/home"; };
  const handleFormsClick: (() => void) = (): void => { location.hash = "#!/forms"; };

  return (
    <React.StrictMode>
      <div className={style.container}>
          <img className={style.logo} src={logo} alt="integrates-logo" onClick={handleLogoClick} />
        <ul>
          <TabItem icon={<i className="icon s7-note2" />} labelText="Formularios" onClick={handleFormsClick} />
        </ul>
        <div className={style.bottomBar}>
          <ul>
            <li onClick={handleEsClick}><a>ES</a></li>
            <li onClick={handleEnClick}><a>EN</a></li>
            <li onClick={handleLogoutClick}><a><span className="icon s7-power" /></a></li>
          </ul>
        </div>
      </div>
    </React.StrictMode>
  );
};

export { sidebar as Sidebar };
