/* eslint react/forbid-component-props: 0 */
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { SquaredCardContainer } from "../../styles/styledComponents";
import { CloudImage } from "../CloudImage";

interface IProps {
  color: string;
  image: string;
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
    c-dkred
    f-375
    mb4
    fw7
    mt0
  `,
})``;

const WhiteParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    white
    f-375
    mb1
    fw7
    mt0
  `,
})``;

const SmallBlackText: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    mt0
    c-fluid-bk
    f5
  `,
})``;

const SmallGrayText: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    mt0
    c-fluid-gray
    f5
  `,
})``;

const ShadowedCard: React.FC<IProps> = ({
  color,
  image,
  number,
  text,
}: IProps): JSX.Element => {
  if (color === "bg-white") {
    return (
      <WhiteCardContainer>
        <SquaredCardContainer className={`${color}`}>
          <CloudImage
            alt={"card-image"}
            src={`${image}`}
            styles={"solution-card-icon mt4"}
          />
          <React.Fragment>
            <RedParagraph>{number}</RedParagraph>
            <SmallBlackText>{text}</SmallBlackText>
          </React.Fragment>
        </SquaredCardContainer>
      </WhiteCardContainer>
    );
  }

  return (
    <WhiteCardContainer>
      <SquaredCardContainer className={`${color}`}>
        <CloudImage
          alt={"card-image"}
          src={`${image}`}
          styles={"solution-card-icon mt4"}
        />
        {color === "bg-black-18" ? (
          <React.Fragment>
            <WhiteParagraph>{number}</WhiteParagraph>
            <SmallGrayText>{text}</SmallGrayText>
          </React.Fragment>
        ) : undefined}
      </SquaredCardContainer>
    </WhiteCardContainer>
  );
};

// eslint-disable-next-line fp/no-mutation
ShadowedCard.defaultProps = {
  number: "",
  text: "",
};

export { ShadowedCard };
