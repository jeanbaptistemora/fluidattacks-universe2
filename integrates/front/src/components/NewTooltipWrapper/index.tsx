import React from "react";
import ReactTooltip from "react-tooltip";
import style from "./index.css";

interface ITooltipWrapperProps {
  children: React.ReactNode;
  message: string;
  placement?: string;
}

export const TooltipWrapper: React.FC<ITooltipWrapperProps> = (
  props: Readonly<ITooltipWrapperProps>
): JSX.Element => {
  const { children, message, placement = "bottom" } = props;

  return (
    <div
      data-class={`${style.tooltip} tc o-90`}
      data-effect={"solid"}
      data-place={placement}
      data-tip={message}
    >
      {children}
      <ReactTooltip delayShow={500} />
    </div>
  );
};
