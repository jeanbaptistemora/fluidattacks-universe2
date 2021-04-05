/* eslint-disable react/forbid-component-props
  --------
  Need it to override default background color based on condition
*/
import _ from "lodash";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { getBgColor } from "components/DataTableNext/formatters/statusFormatter";

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
  const statusCapitalized: string = _.capitalize(status);
  const currentStateBgColor: string = getBgColor(statusCapitalized);

  return (
    <React.StrictMode>
      <span>
        <Point className={currentStateBgColor} />
        &nbsp;{statusCapitalized.split(" ")[0]}
      </span>
    </React.StrictMode>
  );
};

export { PointStatus };
