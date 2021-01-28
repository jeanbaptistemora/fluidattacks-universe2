import React from "react";
import ReactTooltip from "react-tooltip";
import style from "./index.css";

interface ITooltipWrapperProps {
  children: React.ReactNode;
  displayClass?: string;
  message: string;
  placement?: string;
}

export const TooltipWrapper: React.FC<ITooltipWrapperProps> = (
  props: Readonly<ITooltipWrapperProps>
): JSX.Element => {
  const { children, displayClass, message, placement = "bottom" } = props;

  return (
    <div
      className={displayClass}
      data-class={`${style.tooltip} tc o-90`}
      data-effect={"solid"}
      data-html={true}
      data-place={placement}
      data-tip={message}
    >
      {children}
      <ReactTooltip delayShow={500} />
    </div>
  );
};
