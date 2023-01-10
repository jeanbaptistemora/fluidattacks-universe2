import React from "react";

import { Container } from "../Container";
import { Text } from "../Text";

type TVariant = "critical" | "high" | "low" | "medium";

interface ITagScoreProps {
  score: number;
  variant: TVariant;
}

interface IVariant {
  bgColor: string;
  border: string;
  text: string;
}

const variants: Record<TVariant, IVariant> = {
  critical: {
    bgColor: "#b3000f",
    border: "1px solid #b3000f",
    text: "Critical",
  },
  high: {
    bgColor: "#f2182a",
    border: "1px solid #f2182a",
    text: "High",
  },
  low: {
    bgColor: "#ffce00",
    border: "1px solid #ffce00",
    text: "Low",
  },
  medium: {
    bgColor: "#fc9117",
    border: "1px solid #fc9117",
    text: "Medium",
  },
};

const ScoreTag: React.FC<ITagScoreProps> = ({
  score,
  variant,
}): JSX.Element => {
  const { bgColor, border, text } = variants[variant];

  return (
    <Container border={border} br={"5px"} display={"flex"}>
      <Container pb={"2px"} pl={"6px"} pr={"6px"} pt={"2px"}>
        <Text>{score}</Text>
      </Container>
      <Container bgColor={bgColor} pb={"2px"} pl={"6px"} pr={"6px"} pt={"2px"}>
        <Text tone={"light"}>{text}</Text>
      </Container>
    </Container>
  );
};

export { ScoreTag };
