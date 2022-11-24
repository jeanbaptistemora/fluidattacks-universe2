import { decode } from "he";
import { utc } from "moment";
import React from "react";

import { CardFooter } from "./styledComponents";
import type { IVerticalCard } from "./types";

import { AirsLink } from "../AirsLink";
import { Button } from "../Button";
import { CloudImage } from "../CloudImage";
import { Container } from "../Container";
import { Text, Title } from "../Typography";

const VerticalCard: React.FC<IVerticalCard> = ({
  alt,
  author = "",
  link,
  bgColor = "#f4f4f6",
  btnDisplay = "block",
  btnText,
  btnVariant = "tertiary",
  date = "",
  description,
  image,
  minWidth,
  minWidthMd,
  minWidthSm,
  subtitle = "",
  subMinHeight,
  title,
  titleMinHeight,
  width,
  widthMd,
  widthSm,
}): JSX.Element => {
  const fDate = utc(date.toLocaleString()).format("LL");

  if (author && date && subtitle) {
    return (
      <Container
        bgColor={bgColor}
        br={2}
        direction={"column"}
        display={"flex"}
        mh={2}
        minWidth={minWidth}
        minWidthMd={minWidthMd}
        minWidthSm={minWidthSm}
        mv={2}
        width={width}
        widthMd={widthMd}
        widthSm={widthSm}
      >
        {image.startsWith("https") ? (
          <img alt={alt} className={"br2 br--top"} src={image} />
        ) : (
          <Container minHeight={titleMinHeight} ph={3}>
            <CloudImage alt={alt} src={image} styles={"br2 br--top"} />
          </Container>
        )}
        <Container display={"flex"} justify={"around"} ph={3} pt={3}>
          <Text color={"#8f8fa3"} size={"small"}>
            {fDate}
          </Text>
          <Text color={"#8f8fa3"} size={"small"} textAlign={"end"}>
            {author}
          </Text>
        </Container>
        <Container minHeight={titleMinHeight} mv={3} ph={3}>
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
        <Container minHeight={subMinHeight} ph={3}>
          <Title color={"#535365"} level={3} size={"xs"}>
            {decode(subtitle)}
          </Title>
        </Container>
        <Container mv={3} ph={3}>
          <Text color={"#535365"} size={"medium"}>
            {description}
          </Text>
        </Container>
        <CardFooter>
          <Container pb={3} ph={3}>
            <AirsLink href={link}>
              <Button display={btnDisplay} variant={btnVariant}>
                {btnText}
              </Button>
            </AirsLink>
          </Container>
        </CardFooter>
      </Container>
    );
  }

  return (
    <Container
      bgColor={bgColor}
      br={2}
      direction={"column"}
      display={"flex"}
      mh={2}
      minWidth={minWidth}
      minWidthMd={minWidthMd}
      minWidthSm={minWidthSm}
      mv={2}
      width={width}
      widthMd={widthMd}
      widthSm={widthSm}
    >
      {image.startsWith("https") ? (
        <img alt={alt} className={"br2 br--top"} src={image} />
      ) : (
        <Container minHeight={titleMinHeight} ph={3}>
          <CloudImage alt={alt} src={image} styles={"br2 br--top"} />
        </Container>
      )}
      <Container minHeight={titleMinHeight} ph={3} pt={3}>
        <AirsLink href={link}>
          <Title color={"#2e2e38"} hColor={"#bf0b1a"} level={2} size={"small"}>
            {decode(title)}
          </Title>
        </AirsLink>
      </Container>
      <Container mv={3} ph={3}>
        <Text color={"#535365"} size={"medium"}>
          {description}
        </Text>
      </Container>
      <CardFooter>
        <Container pb={3} ph={3}>
          <AirsLink href={link}>
            <Button display={btnDisplay} variant={btnVariant}>
              {btnText}
            </Button>
          </AirsLink>
        </Container>
      </CardFooter>
    </Container>
  );
};

export { VerticalCard };
