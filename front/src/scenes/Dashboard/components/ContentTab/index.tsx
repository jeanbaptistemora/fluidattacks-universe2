import React from "react";
import { NavLink } from "react-router-dom";
import { default as style } from "./index.css";

interface IContentTabProps {
  icon: string;
  id: string;
  link: string;
  title: string;
}

const contentTab: React.FC<IContentTabProps> = (props: IContentTabProps): JSX.Element => (
  <React.StrictMode>
    <li id={props.id} className={style.tab}>
      <NavLink activeClassName={style.active} to={props.link}>
        <i className={props.icon} />
        &nbsp;{props.title}
      </NavLink>
    </li>
  </React.StrictMode>
);

export { contentTab as ContentTab };
