/* eslint react/forbid-component-props: 0 */
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { SquaredCardContainer } from "../../styles/styledComponents";

interface IProps {
  number?: string;
  text?: string;
}

const WhiteCardContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-auto
    center
    pv3
    flex
  `,
})``;

const RedParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    tc
    c-dkred
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
  <WhiteCardContainer>
    <SquaredCardContainer>
      <RedParagraph>{number}</RedParagraph>
      <SmallBlackText>{text}</SmallBlackText>
    </SquaredCardContainer>
  </WhiteCardContainer>
);

// eslint-disable-next-line fp/no-mutation
WhiteShadowedCard.defaultProps = {
  number: "",
  text: "",
};

export { WhiteShadowedCard };
