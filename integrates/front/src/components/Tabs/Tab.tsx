import React from "react";

import { TabLink } from "./styles";

import { TooltipWrapper } from "components/TooltipWrapper";

interface ITabProps {
  id: string;
  link: string;
  title: string;
  tooltip: string;
}

const Tab: React.FC<ITabProps> = (props: ITabProps): JSX.Element => {
  const { tooltip, id, title, link } = props;

  return (
    <li>
      <TooltipWrapper id={`${id}Tooltip`} message={tooltip}>
        <TabLink id={id} to={link}>
          {title}
        </TabLink>
      </TooltipWrapper>
    </li>
  );
};

export { Tab };
