import React from "react";

import { Container, ImageContainer, TextContainer } from "./styledComponents";

import { Paragraph, Title } from "../../../Texts";
import { InteractiveImage } from "../InteractiveImage";

interface IDemoProps {
  description: string;
  image1: string;
  image2: string;
  imageRight: boolean;
  subtitle: string;
  title: string;
}

const DemoBanner: React.FC<IDemoProps> = ({
  description,
  image1,
  image2,
  imageRight,
  subtitle,
  title,
}: IDemoProps): JSX.Element => {
  return (
    <Container>
      {imageRight ? (
        <React.Fragment>
          <TextContainer>
            <Title fColor={"#ff3435"} fSize={"24"}>
              {title}
            </Title>
            <Title fColor={"#2e2e38"} fSize={"36"} marginTop={"1.5"}>
              {subtitle}
            </Title>
            <Paragraph fColor={"#5c5c70"} fSize={"20"} marginTop={"1.5"}>
              {description}
            </Paragraph>
          </TextContainer>
          <ImageContainer margin={imageRight}>
            <InteractiveImage
              image1={`/airs/product-overview/demo-section/${image1}`}
              image2={`/airs/product-overview/demo-section/${image2}`}
              isRight={imageRight}
            />
          </ImageContainer>
        </React.Fragment>
      ) : (
        <React.Fragment>
          <ImageContainer margin={imageRight}>
            <InteractiveImage
              image1={`/airs/product-overview/demo-section/${image1}`}
              image2={`/airs/product-overview/demo-section/${image2}`}
              isRight={imageRight}
            />
          </ImageContainer>
          <TextContainer>
            <Title fColor={"#ff3435"} fSize={"24"}>
              {title}
            </Title>
            <Title fColor={"#2e2e38"} fSize={"36"} marginTop={"1.5"}>
              {subtitle}
            </Title>
            <Paragraph fColor={"#5c5c70"} fSize={"20"} marginTop={"1.5"}>
              {description}
            </Paragraph>
          </TextContainer>
        </React.Fragment>
      )}
    </Container>
  );
};

export { DemoBanner };
