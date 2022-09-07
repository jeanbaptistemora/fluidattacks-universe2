/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable react/jsx-no-bind */
import type { FC, ReactNode } from "react";
import React from "react";
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
  id,
  place,
  tip = "",
  hide = tip === "",
}: Readonly<ITooltipProps>): JSX.Element => (
  <TooltipBox disp={disp} id={id} place={place} tip={tip}>
    {children}
    {hide ? undefined : (
      <ReactTooltip
        delayShow={500}
        id={id}
        overridePosition={(
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
            left: Math.min(
              Math.max(left, 0),
              doc.clientWidth - node.clientWidth
            ),
            top: Math.min(
              Math.max(top, 0),
              doc.clientHeight - node.clientHeight
            ),
          };
        }}
      />
    )}
  </TooltipBox>
);

export type { ITooltipProps };
export { Tooltip };
