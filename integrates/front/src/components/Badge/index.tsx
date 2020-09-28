import React from "react";
import styled, { StyledComponent } from "styled-components";

const StyledBadge: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs<{
  className: string;
}>({
  className:
    "bg-red br4 dib f7 fw7 lh-solid ml2 mr1 nowrap ph2 pv1 relative tc v-top white",
})``;

export interface IBadgeProps {
  children?: string;
}

export const Badge: React.FC<IBadgeProps> = (
  props: Readonly<IBadgeProps>
): JSX.Element => {
  const { children } = props;

  return <StyledBadge>{children}</StyledBadge>;
};
