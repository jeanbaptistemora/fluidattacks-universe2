import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const Container: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-300
    mw-1366
    ph-body
    center
  `,
})``;

const InnerFlexContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    flex-l
  `,
})``;

const ThirdWidthContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  w-34-l
  w-100
  `,
})``;

const Title: StyledComponent<"p", Record<string, unknown>> = styled.p.attrs({
  className: `
    tl
    roboto
    c-black-gray
    fw4
    f5
    mh0
  `,
})``;

const MainText: StyledComponent<"p", Record<string, unknown>> = styled.p.attrs({
  className: `
    neue
    f3
    tl
    fw7
  `,
})``;

const DownloadText: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    t-all-3-eio
    fl
    mv0
  `,
})``;

export {
  Container,
  DownloadText,
  InnerFlexContainer,
  MainText,
  ThirdWidthContainer,
  Title,
};
