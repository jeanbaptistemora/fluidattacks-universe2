/* eslint @typescript-eslint/no-unsafe-member-access: 0*/
import type { FC, ReactNode } from "react";
import React, { useCallback } from "react";
import ReactTooltip from "react-tooltip";

import type { ITooltipBoxProps } from "./styles";
import { TooltipBox } from "./styles";

interface ITooltipPosition {
  left: number;
  top: number;
}

interface ITooltipProps extends ITooltipBoxProps {
  children: ReactNode;
  hide?: boolean;
}

const Tooltip: FC<ITooltipProps> = ({
  children,
  disp,
  effect = "solid",
  id,
  place,
  tip = "",
  hide = tip === "",
}: Readonly<ITooltipProps>): JSX.Element => {
  const handleOverridePosition = useCallback(
    (
      { left, top }: ITooltipPosition,
      _currentEvent,
      _currentTarget,
      node
    ): ITooltipPosition => {
      if (node === null) {
        return { left, top };
      }
      const doc = document.documentElement;

      return {
        left: Math.min(Math.max(left, 0), doc.clientWidth - node.clientWidth),
        top: Math.min(Math.max(top, 0), doc.clientHeight - node.clientHeight),
      };
    },
    []
  );

  return (
    <TooltipBox disp={disp} effect={effect} id={id} place={place} tip={tip}>
      {children}
      {hide ? undefined : (
        <ReactTooltip
          delayShow={500}
          effect={effect}
          id={id}
          overridePosition={handleOverridePosition}
        />
      )}
    </TooltipBox>
  );
};

export type { ITooltipProps };
export { Tooltip };
