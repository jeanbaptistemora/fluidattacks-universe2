import React from "react";
import { NavLink } from "react-router-dom";
import { TooltipWrapper } from "../../../../components/TooltipWrapper/index";
import { default as style } from "./index.css";

interface IContentTabProps {
  icon: string;
  id: string;
  link: string;
  title: string;
  tooltip: string;
}

const contentTab: React.FC<IContentTabProps> = (props: IContentTabProps): JSX.Element => (
  <React.StrictMode>
    <TooltipWrapper message={props.tooltip}>
      <li id={props.id} className={style.tab}>
        <NavLink activeClassName={style.active} to={props.link}>
          <i className={props.icon} />
          &nbsp;{props.title}
        </NavLink>
      </li>
    </TooltipWrapper>
  </React.StrictMode>
);

export { contentTab as ContentTab };
