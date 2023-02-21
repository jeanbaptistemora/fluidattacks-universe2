import type { MouseEventHandler } from "react";

type TDecorations = "none" | "underline";

interface ILinkProps {
  decoration?: TDecorations;
  hoverColor?: string;
  onClick?: MouseEventHandler<HTMLAnchorElement> &
    MouseEventHandler<HTMLDivElement>;
}

export type { ILinkProps, TDecorations };
