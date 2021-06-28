import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const BlueContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    bg-darker-blue
    ba
    bw2
    bc-darker-blue
  `,
})``;

const Container: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-250
    me-1366
    center
    ph-body
    flex-l
    pv6
  `,
})``;

const InnerContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w5-l
    center
  `,
})``;

const Title: StyledComponent<"p", Record<string, unknown>> = styled.p.attrs({
  className: `
    tc
    roboto
    c-black-gray
    fw4
    f5
    ma0
    pv3
  `,
})``;

export { BlueContainer, Container, InnerContainer, Title };
