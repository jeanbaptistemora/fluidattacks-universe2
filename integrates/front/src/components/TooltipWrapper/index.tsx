import React from "react";
import { Trans } from "react-i18next";
import style from "components/TooltipWrapper/index.css";
import { OverlayTrigger, Tooltip } from "react-bootstrap";

interface ITooltipWrapperProps {
  children: React.ReactNode;
  message: string;
  placement?: "left" | "right" | "top";
}

export const TooltipWrapper: React.FC<ITooltipWrapperProps> = (
  props: Readonly<ITooltipWrapperProps>
): JSX.Element => {
  const { children, message, placement = "bottom" } = props;

  return (
    <OverlayTrigger
      delayHide={150}
      delayShow={300}
      key={placement}
      overlay={
        // We need className to override default styles from react-bootstrap
        // eslint-disable-next-line react/forbid-component-props
        <Tooltip className={style.tooltip} id={`tooltip-${placement}`}>
          <Trans>{message}</Trans>
        </Tooltip>
      }
      placement={placement}
    >
      {children}
    </OverlayTrigger>
  );
};
