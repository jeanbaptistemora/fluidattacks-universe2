import _ from "lodash";
import React from "react";
import { NavLink } from "react-router-dom";

import { Badge, IBadgeProps } from "components/Badge";
import { TooltipWrapper } from "components/TooltipWrapper";
import { default as style } from "scenes/Dashboard/components/ContentTab/index.css";

interface IContentTabProps {
  icon: string;
  id: string;
  link: string;
  plus?: {
    config?: IBadgeProps;
    visible: boolean;
  };
  title: string;
  tooltip: string;
}

const contentTab: React.FC<IContentTabProps> = (
  props: IContentTabProps,
): JSX.Element => {
  const { tooltip, id, icon, title, plus } = props;

  return (
    <TooltipWrapper message={tooltip}>
      <li id={id} className={style.tab}>
        <NavLink activeClassName={style.active} to={props.link}>
          <i className={icon} />
          &nbsp;{title}
          {!_.isUndefined(plus) && plus.visible ? (
            <Badge {...plus.config}>pro</Badge>
          ) : undefined}
        </NavLink>
      </li>
    </TooltipWrapper>
  );
};

export { contentTab as ContentTab };
