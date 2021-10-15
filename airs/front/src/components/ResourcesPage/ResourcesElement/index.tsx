/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import { CloudImage } from "../../CloudImage";
import {
  CardInnerContainer,
  CardInnerDescription,
  CardTitle,
  ImageContainer,
  LittleRegularRedButton,
  TextContainer,
} from "../styledComponents";

interface IProps {
  buttonDescription: string;
  description: string;
  direction: string;
  image: string;
  imageSide: string;
  textSide: string;
  title: string;
}

const ResourcesElement: React.FC<IProps> = ({
  buttonDescription,
  description,
  direction,
  image,
  imageSide,
  textSide,
  title,
}: IProps): JSX.Element => (
  <CardInnerContainer>
    <ImageContainer className={imageSide}>
      <CloudImage alt={"Rules image"} src={image} styles={"drop-resources"} />
    </ImageContainer>
    <TextContainer className={textSide}>
      <CardTitle>{title}</CardTitle>
      <CardInnerDescription>{description}</CardInnerDescription>
      <Link to={direction}>
        <LittleRegularRedButton>{buttonDescription}</LittleRegularRedButton>
      </Link>
    </TextContainer>
  </CardInnerContainer>
);

export { ResourcesElement };
