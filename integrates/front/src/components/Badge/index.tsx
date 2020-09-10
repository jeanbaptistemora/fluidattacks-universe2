import { Badge as BootstrapBadge } from "react-bootstrap";
import React from "react";
import style from "components/Badge/index.css";

export interface IBadgeProps {
  responsive?: boolean;
  size?: "sm" | "md";
  children?: string;
}

export const Badge: React.FC<IBadgeProps> = (
  props: Readonly<IBadgeProps>
): JSX.Element => {
  const { children, responsive = false, size = "xs" } = props;

  return (
    <BootstrapBadge
      bsClass={`badge ${style.badge} ${responsive ? style.position : ""} ${
        style[size]
      }`}
    >
      {children}
    </BootstrapBadge>
  );
};
