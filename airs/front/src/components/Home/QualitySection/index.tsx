/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import React from "react";

import {
  BlueContainer,
  Container,
  InnerContainer,
  Title,
} from "./styledComponents";

import { CloudImage } from "../../CloudImage";

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
