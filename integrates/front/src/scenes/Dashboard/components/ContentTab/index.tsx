import React from "react";
import { NavLink } from "react-router-dom";

import { TooltipWrapper } from "components/TooltipWrapper";
import { Tab } from "styles/styledComponents";

interface IContentTabProps {
  icon: string;
  id: string;
  link: string;
  title: string;
  tooltip: string;
}

const contentTab: React.FC<IContentTabProps> = (
  props: IContentTabProps
): JSX.Element => {
  const { tooltip, id, icon, title, link } = props;

  return (
    <TooltipWrapper id={`${id}Tooltip`} message={tooltip}>
      <Tab id={id}>
        <NavLink activeClassName={"nav-active-bg"} to={link}>
          <i className={icon} />
          &nbsp;{title}
        </NavLink>
      </Tab>
    </TooltipWrapper>
  );
};

export { contentTab as ContentTab, IContentTabProps };
