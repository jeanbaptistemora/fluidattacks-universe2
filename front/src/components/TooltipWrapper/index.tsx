import React from "react";
import { OverlayTrigger, Tooltip } from "react-bootstrap";
import { default as style } from "./index.css";

interface ItooltipWrapperProps {
  children: React.ReactNode;
  message: string;
  placement: "top" | "bottom" | "right" | "left";
}

const tooltipWrapper: React.FunctionComponent<ItooltipWrapperProps> = (props: ItooltipWrapperProps): JSX.Element => (
  <React.StrictMode>
    <OverlayTrigger
      key={props.placement}
      delayHide={150}
      delayShow={300}
      overlay={<Tooltip className={style.tooltip} id={`tt-${props.placement}`}>{props.message}</Tooltip>}
      placement={props.placement}
    >
      {props.children}
    </OverlayTrigger>
  </React.StrictMode>
);

export {tooltipWrapper as TooltipWrapper};
