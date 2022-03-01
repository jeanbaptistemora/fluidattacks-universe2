/* eslint-disable react/forbid-component-props
  --------
  Need it to override default background color based on condition
*/
import _ from "lodash";
import React from "react";
import styled from "styled-components";

import { getBgColor } from "utils/colors";

const Point = styled.span`
  border-radius: 50px;
  font-weight: 400;
  padding: 4px 12px;
`;

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
    <Point className={`v-mid ${currentStateBgColor}`}>
      {formatedStatus.split(" ")[0]}
    </Point>
  );
};

const pointStatusFormatter = (value: string): JSX.Element => (
  <PointStatus status={value} />
);

export { pointStatusFormatter, Point, PointStatus };
