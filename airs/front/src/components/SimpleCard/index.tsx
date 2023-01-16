import React from "react";

import type { ISimpleCardProps } from "./types";

import { CloudImage } from "../CloudImage";
import { Container } from "../Container";
import { Text, Title } from "../Typography";

const SimpleCard: React.FC<ISimpleCardProps> = ({
  bgColor,
  bgGradient,
  borderColor,
  description,
  descriptionColor,
  hoverColor,
  hoverShadow,
  image,
  title = "",
  titleColor = "unset",
  titleMinHeight,
  width,
  widthMd,
  widthSm,
}): JSX.Element => {
  if (title) {
    return (
      <Container
        bgColor={bgColor}
        bgGradient={bgGradient}
        borderColor={borderColor}
        br={2}
        direction={"column"}
        display={"flex"}
        hoverColor={hoverColor}
        hoverShadow={hoverShadow}
        mh={2}
        mv={2}
        ph={3}
        pv={3}
        width={width}
        widthMd={widthMd}
        widthSm={widthSm}
      >
        <Container height={"48px"} mv={3} width={"48px"}>
          <CloudImage alt={title} src={image} styles={"w-100 h-100"} />
        </Container>
        <Container minHeight={titleMinHeight}>
          <Title color={titleColor} level={3} size={"small"}>
            {title}
          </Title>
        </Container>
        <Container mv={3}>
          <Text color={descriptionColor} size={"small"}>
            {description}
          </Text>
        </Container>
      </Container>
    );
  }

  return (
    <Container
      bgColor={bgColor}
      bgGradient={bgGradient}
      borderColor={borderColor}
      br={2}
      direction={"column"}
      display={"flex"}
      hoverColor={hoverColor}
      hoverShadow={hoverShadow}
      mh={2}
      mv={2}
      ph={3}
      pv={3}
      width={width}
      widthMd={widthMd}
      widthSm={widthSm}
    >
      <Container center={true} height={"64px"} mv={3} width={"64px"}>
        <CloudImage alt={image} src={image} styles={"w-100 h-100"} />
      </Container>
      <Container mb={3}>
        <Text color={descriptionColor} size={"small"} textAlign={"center"}>
          {description}
        </Text>
      </Container>
    </Container>
  );
};

export { SimpleCard };
