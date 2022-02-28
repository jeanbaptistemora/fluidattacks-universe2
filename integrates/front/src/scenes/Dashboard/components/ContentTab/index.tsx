import React from "react";

import { TooltipWrapper } from "components/TooltipWrapper";
import { Tab } from "styles/styledComponents";

interface IContentTabProps {
  id: string;
  link: string;
  title: string;
  tooltip: string;
}

const ContentTab: React.FC<IContentTabProps> = (
  props: IContentTabProps
): JSX.Element => {
  const { tooltip, id, title, link } = props;

  return (
    <TooltipWrapper id={`${id}Tooltip`} message={tooltip}>
      <Tab id={id} to={link}>
        {title}
      </Tab>
    </TooltipWrapper>
  );
};

export { ContentTab, IContentTabProps };
