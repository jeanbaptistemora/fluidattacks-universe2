/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { decode } from "he";
import { utc } from "moment";
import React from "react";

import { CardFooter } from "./styledComponents";
import type { IVerticalCard } from "./types";

import { AirsLink } from "../AirsLink";
import { Button } from "../Button";
import { Container } from "../Container";
import { Text, Title } from "../Typography";

const VerticalCard: React.FC<IVerticalCard> = ({
  alt,
  author = "",
  link,
  btnText,
  date = "",
  description,
  image,
  subtitle = "",
  title,
  width,
  widthMd,
  widthSm,
}): JSX.Element => {
  const fDate = utc(date.toLocaleString()).format("LL");

  if (author && date && subtitle) {
    return (
      <Container
        bgColor={"#f4f4f6"}
        br={2}
        direction={"column"}
        display={"flex"}
        mh={2}
        mv={2}
        width={width}
        widthMd={widthMd}
        widthSm={widthSm}
      >
        <img alt={alt} className={"br2 br--top"} src={image} />
        <Container ph={3} pv={3}>
          <Container display={"flex"} justify={"around"}>
            <Text color={"#8f8fa3"} size={"small"}>
              {fDate}
            </Text>
            <Text color={"#8f8fa3"} size={"small"} textAlign={"end"}>
              {author}
            </Text>
          </Container>
          <Container mv={3}>
            <AirsLink href={link}>
              <Title
                color={"#2e2e38"}
                hColor={"#bf0b1a"}
                level={2}
                size={"small"}
              >
                {decode(title)}
              </Title>
            </AirsLink>
          </Container>
          <Container>
            <Title color={"#535365"} level={3} size={"xs"}>
              {decode(subtitle)}
            </Title>
          </Container>
          <Container mv={3}>
            <Text color={"#535365"} size={"medium"}>
              {description}
            </Text>
          </Container>
          <CardFooter>
            <AirsLink href={link}>
              <Button display={"block"} variant={"tertiary"}>
                {btnText}
              </Button>
            </AirsLink>
          </CardFooter>
        </Container>
      </Container>
    );
  }

  return (
    <Container
      bgColor={"#f4f4f6"}
      br={2}
      direction={"column"}
      display={"flex"}
      mh={2}
      mv={2}
      width={width}
      widthMd={widthMd}
      widthSm={widthSm}
    >
      <img alt={alt} className={"br2 br--top"} src={image} />
      <Container ph={3} pv={3}>
        <Container mb={3}>
          <AirsLink href={link}>
            <Title
              color={"#2e2e38"}
              hColor={"#bf0b1a"}
              level={2}
              size={"small"}
            >
              {decode(title)}
            </Title>
          </AirsLink>
        </Container>
        <Container mb={3}>
          <Text color={"#535365"} size={"medium"}>
            {description}
          </Text>
        </Container>
        <CardFooter>
          <AirsLink href={link}>
            <Button display={"block"} variant={"tertiary"}>
              {btnText}
            </Button>
          </AirsLink>
        </CardFooter>
      </Container>
    </Container>
  );
};

export { VerticalCard };
