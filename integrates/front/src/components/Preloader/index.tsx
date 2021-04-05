import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import loadingAnim from "resources/loading.gif";

const StyledDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "bottom-15 fixed left-5 o-80 z-9999",
})``;

const StyledImg: StyledComponent<
  "img",
  Record<string, unknown>
> = styled.img.attrs<{
  className: string;
}>({
  className: "img-box",
})``;

export const Preloader: React.FC = (): JSX.Element => (
  <StyledDiv id={"full_loader"}>
    <StyledImg alt={"Loading animation"} src={loadingAnim} />
  </StyledDiv>
);
