/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { RegularRedButton } from "../../../styles/styledComponents";
import { CloudImage } from "../../CloudImage";

interface IProps {
  buttonText: string;
  cardType: string;
  description: string;
  image: string;
  language: string;
  title: string;
  urlCard: string;
}

const CardContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    fadein
    br3
    bs-btm-h-10
    hv-card
    mb5
    relative
    dt-ns
    mt0-ns
    center
    bg-white
    w-resources-card
    h-resources-card
    all-card
    `,
})``;

const WebinarImageContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    br3
    br--top
    `,
})``;

const WebinarLanguage: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: `
    f7
    white
    bg-moon-gray
    br3
    pv2
    ph3
    ma0
    fw7
    `,
})``;

const CardTextContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    ph2
    mh1
    `,
})``;

const CardTitle: StyledComponent<
  "h1",
  Record<string, unknown>
> = styled.h1.attrs({
  className: `
    c-fluid-bk
    mb0
    f3
    fw8
    tc
    lh2
    pb3
    h-resources-card-title
    `,
})``;

const CardDescription: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    c-fluid-bk
    fw3
    f5
    mv0
    h-resources-card-description
    `,
})``;

const ButtonContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pv4
    tc
    `,
})``;

const ResourcesCard: React.FC<IProps> = ({
  buttonText,
  cardType,
  description,
  image,
  language,
  title,
  urlCard,
}: IProps): JSX.Element => (
  <CardContainer className={cardType}>
    {cardType === "webinar-card" ? (
      <WebinarImageContainer className={image}>
        <div className={"pa3"}>
          <WebinarLanguage>{language}</WebinarLanguage>
        </div>
      </WebinarImageContainer>
    ) : (
      <CloudImage alt={language} src={image} styles={"br3 br--top"} />
    )}
    <CardTextContainer>
      <CardTitle>{title}</CardTitle>
      <CardDescription>{description}</CardDescription>
    </CardTextContainer>
    <ButtonContainer>
      <Link to={urlCard}>
        <RegularRedButton>{buttonText}</RegularRedButton>
      </Link>
    </ButtonContainer>
  </CardContainer>
);

export { ResourcesCard };
