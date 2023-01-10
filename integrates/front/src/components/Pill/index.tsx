import React from "react";

import { Container } from "../Container";
import { Text } from "../Text";
import type { TColor } from "../Text";

type TVariant = "darkRed" | "orange" | "red" | "yellow";

interface ITagScoreProps {
  textL: string;
  textR: string;
  variant: TVariant;
}

interface IVariant {
  bgColor: string;
  border: string;
  tone: TColor;
}

const variants: Record<TVariant, IVariant> = {
  darkRed: {
    bgColor: "#b3000f",
    border: "1px solid #b3000f",
    tone: "light",
  },
  orange: {
    bgColor: "#fc9117",
    border: "1px solid #fc9117",
    tone: "dark",
  },
  red: {
    bgColor: "#f2182a",
    border: "1px solid #f2182a",
    tone: "light",
  },
  yellow: {
    bgColor: "#ffce00",
    border: "1px solid #ffce00",
    tone: "dark",
  },
};

const Pill: React.FC<ITagScoreProps> = ({
  textL,
  textR,
  variant,
}): JSX.Element => {
  const { bgColor, border, tone } = variants[variant];

  return (
    <Container display={"inline-block"}>
      <Container border={border} br={"5px"} display={"flex"}>
        <Container pb={"2px"} pl={"6px"} pr={"6px"} pt={"2px"}>
          <Text>{textL}</Text>
        </Container>
        <Container
          bgColor={bgColor}
          pb={"2px"}
          pl={"6px"}
          pr={"6px"}
          pt={"2px"}
        >
          <Text tone={tone}>{textR}</Text>
        </Container>
      </Container>
    </Container>
  );
};

export { Pill };
