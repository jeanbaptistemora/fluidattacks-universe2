/* eslint react/jsx-no-bind:0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import React, { useCallback } from "react";

import type { IHeroProps } from "./types";

import { AirsLink } from "../AirsLink";
import { Button } from "../Button";
import { CloudImage } from "../CloudImage";
import { Container } from "../Container";
import { Text, Title } from "../Typography";

const Hero: React.FC<IHeroProps> = ({
  bgColor,
  button1Link,
  button1Text,
  button2Link,
  button2Text,
  image,
  matomoAction,
  paragraph,
  size = "big",
  sizeMd,
  sizeSm,
  title,
  variant = "center",
}): JSX.Element => {
  const { trackEvent } = useMatomo();

  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({
      action: "cta-banner-click",
      category: `${matomoAction}`,
    });
  }, [matomoAction, trackEvent]);

  if (variant === "center") {
    return (
      <Container bgColor={bgColor} ph={4} pv={5}>
        <Container
          align={"center"}
          center={true}
          display={"flex"}
          justify={"center"}
          maxWidth={"1440px"}
          wrap={"wrap"}
        >
          <Container width={"50%"} widthMd={"100%"}>
            <Title
              color={"#2e2e38"}
              level={1}
              mb={3}
              size={size}
              sizeMd={sizeMd}
              sizeSm={sizeSm}
            >
              {title}
            </Title>
            <Text color={"#65657b"} size={"big"}>
              {paragraph}
            </Text>
            <Container
              display={"flex"}
              justify={"start"}
              justifyMd={"center"}
              justifySm={"unset"}
              mv={3}
              wrap={"wrap"}
            >
              <Container pv={1} width={"auto"} widthSm={"100%"}>
                <AirsLink href={button1Link}>
                  <Button
                    display={"block"}
                    onClick={matomoFreeTrialEvent}
                    variant={"primary"}
                  >
                    {button1Text}
                  </Button>
                </AirsLink>
              </Container>
              <Container ph={3} phSm={0} pv={1} width={"auto"} widthSm={"100%"}>
                <AirsLink href={button2Link}>
                  <Button display={"block"} variant={"tertiary"}>
                    {button2Text}
                  </Button>
                </AirsLink>
              </Container>
            </Container>
          </Container>
          <Container
            display={"flex"}
            justify={"center"}
            width={"50%"}
            widthMd={"100%"}
          >
            <CloudImage alt={title} src={image} />
          </Container>
        </Container>
      </Container>
    );
  }

  return (
    <Container bgColor={bgColor} display={"flex"} justify={"end"} pv={5}>
      <Container
        align={"center"}
        display={"flex"}
        justify={"end"}
        maxWidth={"1440px"}
        mr={0}
        wrap={"wrap"}
      >
        <Container width={"50%"} widthMd={"100%"}>
          <Title
            color={"#2e2e38"}
            level={1}
            mb={3}
            size={size}
            sizeMd={sizeMd}
            sizeSm={sizeSm}
          >
            {title}
          </Title>
          <Text color={"#65657b"} size={"big"}>
            {paragraph}
          </Text>
          <Container
            display={"flex"}
            justify={"start"}
            justifyMd={"center"}
            justifySm={"unset"}
            mv={3}
            wrap={"wrap"}
          >
            <Container pv={1} width={"auto"} widthSm={"100%"}>
              <AirsLink href={button1Link}>
                <Button
                  display={"block"}
                  onClick={matomoFreeTrialEvent}
                  variant={"primary"}
                >
                  {button1Text}
                </Button>
              </AirsLink>
            </Container>
            <Container ph={3} phSm={0} pv={1} width={"auto"} widthSm={"100%"}>
              <AirsLink href={button2Link}>
                <Button display={"block"} variant={"tertiary"}>
                  {button2Text}
                </Button>
              </AirsLink>
            </Container>
          </Container>
        </Container>
        <Container
          display={"flex"}
          justify={"center"}
          width={"50%"}
          widthMd={"100%"}
        >
          <CloudImage alt={title} src={image} />
        </Container>
      </Container>
    </Container>
  );
};

export { Hero };
