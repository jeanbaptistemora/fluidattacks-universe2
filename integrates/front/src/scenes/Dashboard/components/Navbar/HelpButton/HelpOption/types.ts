import type { IconProp } from "@fortawesome/fontawesome-svg-core";
import type { MouseEventHandler } from "react";

interface IHelpOptionProps {
  description: string;
  icon: IconProp;
  onClick?: MouseEventHandler<HTMLButtonElement>;
  title: string;
}

export type { IHelpOptionProps };
