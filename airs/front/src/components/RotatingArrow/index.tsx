/* eslint react/forbid-component-props: 0 */
import { faAngleDown } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { FontAwesomeContainerSmall } from "../../styles/styledComponents";

interface IProps {
  isTouch: boolean;
}

const RotatingArrow: React.FC<IProps> = ({ isTouch }: IProps): JSX.Element => (
  <FontAwesomeContainerSmall>
    <FontAwesomeIcon
      className={"c-c-fluid-gray t-all-linear-3"}
      icon={faAngleDown}
      style={
        isTouch
          ? {
              transform: "rotate(180deg)",
            }
          : undefined
      }
    />
  </FontAwesomeContainerSmall>
);

export { RotatingArrow };
