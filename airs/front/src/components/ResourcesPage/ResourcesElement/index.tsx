/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import { RegularRedButton } from "../../../styles/styledComponents";
import { CloudImage } from "../../CloudImage";
import {
  CardInnerContainer,
  CardInnerDescription,
  CardTitle,
  ImageContainer,
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
        <RegularRedButton>{buttonDescription}</RegularRedButton>
      </Link>
    </TextContainer>
  </CardInnerContainer>
);

export { ResourcesElement };
