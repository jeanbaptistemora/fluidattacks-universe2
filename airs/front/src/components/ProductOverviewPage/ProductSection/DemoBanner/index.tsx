import React from "react";

import {
  BannerContainer,
  CardContainer,
  ImageContainer,
  TextContainer,
} from "./styledComponents";

import { Paragraph, Title } from "../../../Texts";
import { InteractiveImage } from "../InteractiveImage";

interface IDemoProps {
  description: string;
  hasHotSpot: boolean;
  image1: string;
  image2: string;
  imageRight: boolean;
  subtitle: string;
  title: string;
}

const DemoBanner: React.FC<IDemoProps> = ({
  description,
  hasHotSpot,
  image1,
  image2,
  imageRight,
  subtitle,
  title,
}: IDemoProps): JSX.Element => {
  return (
    <React.Fragment>
      {imageRight ? (
        <BannerContainer>
          <TextContainer>
            <Title fColor={"#ff3435"} fSize={"20"}>
              {title}
            </Title>
            <Title fColor={"#2e2e38"} fSize={"24"} marginTop={"1.5"}>
              {subtitle}
            </Title>
            <Paragraph fColor={"#5c5c70"} fSize={"16"} marginTop={"1.5"}>
              {description}
            </Paragraph>
          </TextContainer>
          <ImageContainer margin={imageRight}>
            <InteractiveImage
              hasHotSpot={hasHotSpot}
              image1={`/airs/platform/demo-section/${image1}`}
              image2={`/airs/platform/demo-section/${image2}`}
              isRight={imageRight}
            />
          </ImageContainer>
        </BannerContainer>
      ) : (
        <BannerContainer>
          <ImageContainer margin={imageRight}>
            <InteractiveImage
              hasHotSpot={hasHotSpot}
              image1={`/airs/platform/demo-section/${image1}`}
              image2={`/airs/platform/demo-section/${image2}`}
              isRight={imageRight}
            />
          </ImageContainer>
          <TextContainer>
            <Title fColor={"#ff3435"} fSize={"20"}>
              {title}
            </Title>
            <Title fColor={"#2e2e38"} fSize={"24"} marginTop={"1.5"}>
              {subtitle}
            </Title>
            <Paragraph fColor={"#5c5c70"} fSize={"16"} marginTop={"1.5"}>
              {description}
            </Paragraph>
          </TextContainer>
        </BannerContainer>
      )}
      <CardContainer>
        <TextContainer>
          <Title fColor={"#ff3435"} fSize={"20"}>
            {title}
          </Title>
          <Title fColor={"#2e2e38"} fSize={"24"} marginTop={"1.5"}>
            {subtitle}
          </Title>
          <Paragraph fColor={"#5c5c70"} fSize={"16"} marginTop={"1.5"}>
            {description}
          </Paragraph>
        </TextContainer>
        <ImageContainer margin={false}>
          <InteractiveImage
            hasHotSpot={hasHotSpot}
            image1={`/airs/platform/demo-section/${image1}`}
            image2={`/airs/platform/demo-section/${image2}`}
            isRight={false}
          />
        </ImageContainer>
      </CardContainer>
    </React.Fragment>
  );
};

export { DemoBanner };
