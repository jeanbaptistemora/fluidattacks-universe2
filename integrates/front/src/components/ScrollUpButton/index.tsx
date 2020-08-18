import React from "react";
/*
 * Disabling here is necessary because there are currently no available
 * type definitions for neither this nor any other 3rd-party scroll-up
 * components.
 */
// @ts-expect-error: Explanation above
import ScrollUp from "react-scroll-up";
import style from "./index.css";

interface IScrollUPButtonProps {
  visibleAt: number;
}

export const ScrollUpButton: React.FC<IScrollUPButtonProps> = (
  props: Readonly<IScrollUPButtonProps>
): JSX.Element => {
  const { visibleAt } = props;

  return (
    <ScrollUp duration={400} showUnder={visibleAt}>
      <span className={style.container} id={"scroll-up"} />
    </ScrollUp>
  );
};
