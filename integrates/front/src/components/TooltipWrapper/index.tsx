import React from "react";
import ReactTooltip from "react-tooltip";

import style from "./index.css";

interface ITooltipWrapperProps {
  children: React.ReactNode;
  displayClass?: string;
  id: string;
  message: string;
  placement?: "bottom" | "left" | "right" | "top";
}

export const TooltipWrapper: React.FC<ITooltipWrapperProps> = (
  props: Readonly<ITooltipWrapperProps>
): JSX.Element => {
  const { children, displayClass, id, message, placement = "bottom" } = props;

  return (
    <div
      className={displayClass}
      data-class={`${style.tooltip} tc o-70`}
      data-effect={"solid"}
      data-for={id}
      data-html={true}
      data-place={placement}
      data-tip={message}
    >
      {children}
      <ReactTooltip delayShow={500} id={id} />
    </div>
  );
};
