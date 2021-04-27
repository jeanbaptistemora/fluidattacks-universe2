/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { CloudImage } from "../../CloudImage";

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

const QualitySection: React.FC = (): JSX.Element => (
  <BlueContainer>
    <Container>
      <InnerContainer className={"ml-auto-l mr0-l tc"}>
        <Title>{"CORPORATE MEMBER OF"}</Title>
        <CloudImage
          alt={"Logo OWASP"}
          src={"owasp-logo"}
          styles={"tc w4 ba bg-white br3 bc-gray-64"}
        />
      </InnerContainer>
      <InnerContainer className={"mr-auto-l ml0-l tc"}>
        <Title>{"OUR PUBLIC REVIEWS"}</Title>
        <CloudImage
          alt={"Logo OWASP"}
          src={"clutch-review"}
          styles={"tc w4 ba br3 bc-gray-64 pa2 bg-white"}
        />
      </InnerContainer>
    </Container>
  </BlueContainer>
);

export { QualitySection };
