import React from "react";

import type { IPresentationCardProps } from "./types";

import { CloudImage } from "../CloudImage";
import { Container } from "../Container";
import { Text } from "../Typography";

const PresentationCard: React.FC<IPresentationCardProps> = ({
  image,
  text,
}): JSX.Element => {
  return (
    <Container
      align={"center"}
      borderColor={"#dddde3"}
      br={2}
      display={"flex"}
      height={"100px"}
      hoverShadow={true}
      maxWidth={"350px"}
      ph={3}
      pv={3}
    >
      <Container mr={3} width={"40%"}>
        <CloudImage
          alt={image}
          isProfile={true}
          src={image}
          styles={"w-100 h-100"}
        />
      </Container>
      <Container>
        <Text color={"#2e2e38"}>{text}</Text>
      </Container>
    </Container>
  );
};

export { PresentationCard };
