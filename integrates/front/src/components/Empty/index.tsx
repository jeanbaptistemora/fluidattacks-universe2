import React from "react";

import type { IEmptyProps } from "./types";

import { Container } from "components/Container";
import { Lottie } from "components/Icon";
import { Text } from "components/Text";
import { redLoader } from "resources";

const Empty: React.FC<IEmptyProps> = ({
  loading = true,
  srcImage,
  subtitle,
  title,
}): JSX.Element => {
  return (
    <Container pb={"4rem"} pt={"4rem"}>
      <Container display={"flex"} justify={"center"}>
        <Container maxWidth={"200px"}>
          <img alt={srcImage} src={srcImage} />
        </Container>
      </Container>
      <Container
        align={"center"}
        display={"flex"}
        justify={"center"}
        pb={"12px"}
        scroll={"none"}
      >
        {loading ? <Lottie animationData={redLoader} size={24} /> : undefined}
        <Text disp={"inline"} fw={7} size={"medium"}>
          {title}
        </Text>
      </Container>
      <Container width={"100%"}>
        <Text size={"medium"} ta={"center"}>
          {subtitle}
        </Text>
      </Container>
    </Container>
  );
};

export { Empty };
