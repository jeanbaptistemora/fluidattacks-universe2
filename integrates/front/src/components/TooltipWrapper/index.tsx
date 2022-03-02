/* eslint-disable react/jsx-no-bind, fp/no-mutation, no-param-reassign */
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
      data-for={id}
      data-html={true}
      data-place={placement}
      data-tip={message}
    >
      {children}
      <ReactTooltip
        delayShow={500}
        id={id}
        overridePosition={(
          { left, top },
          _currentEvent,
          _currentTarget,
          node
        ): { left: number; top: number } => {
          const doc = document.documentElement;
          if (node !== null) {
            left = Math.min(doc.clientWidth - node.clientWidth, left);
            top = Math.min(doc.clientHeight - node.clientHeight, top);
            left = Math.max(0, left);
            top = Math.max(0, top);
          }

          return { left, top };
        }}
      />
    </div>
  );
};
