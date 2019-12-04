import React from "react";
/**
 * Disabling here is necessary because
 * there are currently no available type definitions for
 * neither this nor any other 3rd-party scroll-up components
 */
// @ts-ignore
import ScrollUp from "react-scroll-up";
import { default as style } from "./index.css";

interface IScrollUPButtonProps {
  visibleAt: number;
}

const scrollUpButton: React.FC<IScrollUPButtonProps> = (props: IScrollUPButtonProps): JSX.Element => (
  <React.StrictMode>
    <ScrollUp showUnder={props.visibleAt} duration={400}>
      <span className={style.container} />
    </ScrollUp>
  </React.StrictMode>
);

export { scrollUpButton as ScrollUpButton };
