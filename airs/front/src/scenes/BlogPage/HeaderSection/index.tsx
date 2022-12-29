import React from "react";

import type { IHeaderProps } from "./types";

import { AirsLink } from "../../../components/AirsLink";
import { Button } from "../../../components/Button";
import { Container } from "../../../components/Container";
import { Text, Title } from "../../../components/Typography";
import { capitalizePlainString } from "../../../utils/utilities";

const HeaderSection: React.FC<IHeaderProps> = ({
  category,
  description = "",
  image,
  subtitle,
  title,
}): JSX.Element => {
  return (
    <Container bgColor={"#2e2e38"} ph={4} pv={5}>
      <Container center={true} maxWidth={"1000px"}>
        <AirsLink href={`/blog/categories/${category}`}>
          <Button variant={"darkSecondary"}>
            {capitalizePlainString(category)}
          </Button>
        </AirsLink>
        <Title color={"#fff"} level={1} mt={3} size={"big"} sizeSm={"medium"}>
          {title}
        </Title>
        <Title color={"#fff"} level={2} mt={3} size={"small"}>
          {subtitle}
        </Title>
        {description ? (
          <Text color={"#b0b0bf"} mt={3} size={"medium"}>
            {description}
          </Text>
        ) : undefined}
        <Container pt={5} width={"100%"}>
          <img
            alt={`solution ${title}`}
            className={"w-100 h-100"}
            src={image}
          />
        </Container>
      </Container>
    </Container>
  );
};

export { HeaderSection };
