/* eslint react/forbid-component-props: 0 */
import React from "react";
import { IoIosArrowDown } from "react-icons/io";

import { IconContainerSmall } from "../../styles/styledComponents";

interface IProps {
  isTouch: boolean;
}

const RotatingArrow: React.FC<IProps> = ({ isTouch }: IProps): JSX.Element => (
  <IconContainerSmall>
    <IoIosArrowDown
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
