/* eslint react/forbid-component-props: 0 */
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import {
  FullWidthContainer,
  SquaredCardContainer,
} from "../../styles/styledComponents";

interface IProps {
  number?: string;
  text?: string;
}

const RedParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    tc
    c-hovered-red
    f-375
    mb4
    fw7
  `,
})``;

const SmallBlackText: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    tc
    c-fluid-bk
    f5
  `,
})``;

const WhiteShadowedCard: React.FC<IProps> = ({
  number,
  text,
}: IProps): JSX.Element => (
  <FullWidthContainer className={"pv3 flex-l"}>
    <SquaredCardContainer>
      <RedParagraph>{number}</RedParagraph>
      <SmallBlackText>{text}</SmallBlackText>
    </SquaredCardContainer>
  </FullWidthContainer>
);

// eslint-disable-next-line fp/no-mutation
WhiteShadowedCard.defaultProps = {
  number: "",
  text: "",
};

export { WhiteShadowedCard };
