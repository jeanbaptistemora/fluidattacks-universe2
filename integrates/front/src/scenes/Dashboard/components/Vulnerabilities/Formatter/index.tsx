/* eslint-disable react/forbid-component-props
  --------
  Need it to override default background color based on condition
*/
import _ from "lodash";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { getBgColor } from "utils/colors";

const Point: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs<{
  className: string;
}>({
  className: "br-100 f5 paPoint",
})``;

interface IPointStatus {
  status: string;
}

const PointStatus: React.FC<IPointStatus> = ({
  status,
}: IPointStatus): JSX.Element => {
  const formatedStatus: string =
    _.upperCase(status) === "OK" ? _.upperCase(status) : _.capitalize(status);
  const currentStateBgColor: string = getBgColor(_.capitalize(status));

  return (
    <React.StrictMode>
      <span>
        <Point className={`v-mid ${currentStateBgColor}`} />
        <span className={"v-mid"}>&nbsp;{formatedStatus.split(" ")[0]}</span>
      </span>
    </React.StrictMode>
  );
};

const pointStatusFormatter = (value: string): JSX.Element => (
  <div className={"flex flex-wrap"}>
    <div>
      <p className={"dib ma0 v-btm"}>
        <PointStatus status={value} />
      </p>
    </div>
  </div>
);

export { pointStatusFormatter, Point, PointStatus };
