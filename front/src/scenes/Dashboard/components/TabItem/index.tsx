import React from "react";
import { LinkProps, NavLink } from "react-router-dom";
import { default as style } from "./index.css";

interface ITabItemProps extends LinkProps {
  icon: JSX.Element;
  label: string;
}

const tabItem: React.FC<ITabItemProps> = (props: ITabItemProps): JSX.Element => (
  <React.StrictMode>
    <li className={style.container}>
      <NavLink to={props.to} activeClassName={style.active}>
        <div className={style.item}>{props.icon}<span className={style.label}>{props.label}</span></div>
      </NavLink>
    </li>
  </React.StrictMode>
);

export { tabItem as TabItem };
