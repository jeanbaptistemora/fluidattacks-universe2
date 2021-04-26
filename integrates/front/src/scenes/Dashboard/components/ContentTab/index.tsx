import _ from "lodash";
import React from "react";
import { NavLink } from "react-router-dom";

import { Badge } from "components/Badge";
import type { IBadgeProps } from "components/Badge";
import { TooltipWrapper } from "components/TooltipWrapper";
import { Tab } from "styles/styledComponents";

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
  props: IContentTabProps
): JSX.Element => {
  const { tooltip, id, icon, title, plus, link } = props;

  return (
    <TooltipWrapper id={`${id}Tooltip`} message={tooltip}>
      <Tab id={id}>
        <NavLink activeClassName={"nav-active-bg"} to={link}>
          <i className={icon} />
          &nbsp;{title}
          {!_.isUndefined(plus) && plus.visible ? (
            // Next annotation needed so no new React elements have to be created
            // eslint-disable-next-line react/jsx-props-no-spreading
            <Badge {...plus.config}>{"pro"}</Badge>
          ) : undefined}
        </NavLink>
      </Tab>
    </TooltipWrapper>
  );
};

export { contentTab as ContentTab, IContentTabProps };
