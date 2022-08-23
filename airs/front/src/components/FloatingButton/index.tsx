/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import { FloatButton } from "./styledComponents";

interface IFloatingButton {
  bgColor: string;
  color: string;
  text: string;
  to: string;
  yPosition: string;
}

const FloatingButton: React.FC<IFloatingButton> = ({
  bgColor,
  color,
  text,
  to,
  yPosition,
}: IFloatingButton): JSX.Element => {
  return (
    <Link className={"no-underline"} to={to}>
      <FloatButton bgColor={bgColor} color={color} yPosition={yPosition}>
        {text}
      </FloatButton>
    </Link>
  );
};

export { FloatingButton };
