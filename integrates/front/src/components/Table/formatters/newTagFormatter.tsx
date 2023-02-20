import React from "react";

import { LittleFlag } from "./styles";

import { Container } from "components/Container";
import { Text } from "components/Text";

export function newTagFormatter(text: string): JSX.Element {
  return (
    <Container display={"inline-block"}>
      <Container align={"center"} display={"flex"}>
        <Text disp={"inline-block"} mr={1}>
          {text}
        </Text>
        <LittleFlag>{"New"}</LittleFlag>
      </Container>
    </Container>
  );
}
