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
      display={"flex"}
      height={"100px"}
      hoverShadow={true}
      maxWidth={"350px"}
      ph={3}
      pv={3}
    >
      <Container height={"100%"} mr={3} width={"25%"}>
        <CloudImage alt={image} src={image} styles={"w-100 h-100 br-100"} />
      </Container>
      <Container width={"75%"}>
        <Text color={"#2e2e38"}>{text}</Text>
      </Container>
    </Container>
  );
};

export { PresentationCard };
