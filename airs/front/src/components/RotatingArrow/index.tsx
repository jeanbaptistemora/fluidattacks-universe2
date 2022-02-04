/* eslint react/forbid-component-props: 0 */
import React from "react";
import { RiArrowDownSFill } from "react-icons/ri";

import { IconContainerSmall } from "../../styles/styledComponents";

interface IProps {
  isTouch: boolean;
}

const RotatingArrow: React.FC<IProps> = ({ isTouch }: IProps): JSX.Element => (
  <IconContainerSmall>
    <RiArrowDownSFill
      className={"c-c-fluid-gray t-all-linear-3"}
      style={
        isTouch
          ? {
              transform: "rotate(180deg)",
            }
          : undefined
      }
    />
  </IconContainerSmall>
);

export { RotatingArrow };
