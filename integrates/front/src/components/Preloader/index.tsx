import React from "react";
import loadingAnim from "resources/loading.gif";
import styled, { StyledComponent } from "styled-components";

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
