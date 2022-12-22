type TDecorations = "none" | "underline";

interface ILinkProps {
  decoration?: TDecorations;
  hoverColor?: string;
}

export type { ILinkProps, TDecorations };
