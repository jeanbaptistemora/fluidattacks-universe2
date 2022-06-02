import React from "react";

import { TabLink } from "./styles";

import { TooltipWrapper } from "components/TooltipWrapper";

interface ITabProps {
  id: string;
  link: string;
  tooltip?: string;
}

const Tab: React.FC<ITabProps> = ({
  children,
  id,
  link,
  tooltip = "",
}: Readonly<React.PropsWithChildren<ITabProps>>): JSX.Element => {
  return (
    <li>
      <TooltipWrapper id={`${id}Tooltip`} message={tooltip}>
        <TabLink id={id} to={link}>
          {children}
        </TabLink>
      </TooltipWrapper>
    </li>
  );
};

export { Tab };
