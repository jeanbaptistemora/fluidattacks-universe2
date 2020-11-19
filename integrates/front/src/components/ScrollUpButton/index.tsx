import React from "react";
import ScrollUp from "react-scroll-up";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const StyledScrollUp: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs<{
  className: string;
}>({
  className:
    "bg-black bottom-9 br3 fixed o-60 ph2 pv0 right3 su-c su-dib " +
    "su-icon su-icon-f su-v-mid white",
})``;

interface IScrollUPButtonProps {
  visibleAt: number;
}

export const ScrollUpButton: React.FC<IScrollUPButtonProps> = (
  props: Readonly<IScrollUPButtonProps>
): JSX.Element => {
  const { visibleAt } = props;

  return (
    <ScrollUp duration={400} showUnder={visibleAt}>
      <StyledScrollUp id={"scroll-up"} />
    </ScrollUp>
  );
};
