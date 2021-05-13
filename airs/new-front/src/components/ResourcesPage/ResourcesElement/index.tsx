/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { RegularRedButton } from "../../../styles/styledComponents";
import { CloudImage } from "../../CloudImage";

interface IProps {
  buttonDescription: string;
  description: string;
  direction: string;
  image: string;
  imageSide: string;
  textSide: string;
  title: string;
}

const CardContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
      ba1
      mb3
      relative
      dt-ns
      mt0-ns
      pr3-ns
      pl3-ns
      pt3
      ma-auto
      pt3
      ml-auto
      mr-auto
    `,
})``;

const CardTitle: StyledComponent<
  "h2",
  Record<string, unknown>
> = styled.h2.attrs({
  className: `
    f3
    lh-solid
    c-fluid-bk
    roboto
    `,
})``;

const CardDescription: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    fw3
    f4
    c-fluid-bk
    roboto
    `,
})``;

const ImageContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
      tc
      w-50-l
      mb5
      ml-auto
      mr-auto
    `,
})``;

const TextContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
      tl-l
      tc
      w-50-l
      mw6
      ml-auto
      mr-auto
      pt3-l
      ph0-ns
      ph3
    `,
})``;

const ResourcesElement: React.FC<IProps> = ({
  buttonDescription,
  description,
  direction,
  image,
  imageSide,
  textSide,
  title,
}: IProps): JSX.Element => (
  <CardContainer>
    <ImageContainer className={imageSide}>
      <CloudImage alt={"Rules image"} src={image} styles={"drop-resources"} />
    </ImageContainer>
    <TextContainer className={textSide}>
      <CardTitle>{title}</CardTitle>
      <CardDescription>{description}</CardDescription>
      <Link to={direction}>
        <RegularRedButton>{buttonDescription}</RegularRedButton>
      </Link>
    </TextContainer>
  </CardContainer>
);

export { ResourcesElement };
