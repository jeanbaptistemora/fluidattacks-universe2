/* eslint react/jsx-no-bind:0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import React, { useCallback } from "react";

import type { IHeroProps, IHeroTone, THeroTone } from "./types";

import { AirsLink } from "../AirsLink";
import { Button } from "../Button";
import { CloudImage } from "../CloudImage";
import { Container } from "../Container";
import { Text, Title } from "../Typography";

const Hero: React.FC<IHeroProps> = ({
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
  tone = "light",
  variant = "center",
}): JSX.Element => {
  const { trackEvent } = useMatomo();

  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({
      action: "cta-banner-click",
      category: `${matomoAction}`,
    });
  }, [matomoAction, trackEvent]);

  const tones: Record<THeroTone, IHeroTone> = {
    dark: {
      bgColor: "#25252d",
      button1: "primary",
      button2: "darkTertiary",
      paragraphColor: "#b0b0bf",
      titleColor: "#fafafa",
    },
    light: {
      bgColor: "#f4f4f6",
      button1: "primary",
      button2: "tertiary",
      paragraphColor: "#65657b",
      titleColor: "#2e2e38",
    },
  };

  if (variant === "center") {
    return (
      <Container bgColor={tones[tone].bgColor} ph={4} pv={5}>
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
              color={tones[tone].titleColor}
              level={1}
              mb={3}
              size={size}
              sizeMd={sizeMd}
              sizeSm={sizeSm}
            >
              {title}
            </Title>
            <Text color={tones[tone].paragraphColor} size={"big"}>
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
                <AirsLink decoration={"none"} href={button1Link}>
                  <Button
                    display={"block"}
                    onClick={matomoFreeTrialEvent}
                    variant={tones[tone].button1}
                  >
                    {button1Text}
                  </Button>
                </AirsLink>
              </Container>
              <Container ph={3} phSm={0} pv={1} width={"auto"} widthSm={"100%"}>
                <AirsLink href={button2Link}>
                  <Button display={"block"} variant={tones[tone].button2}>
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
    <Container bgColor={tones[tone].bgColor} display={"flex"} justify={"end"}>
      <Container
        align={"center"}
        display={"flex"}
        justify={"end"}
        maxWidth={"1740px"}
        mr={0}
        wrap={"wrap"}
      >
        <Container
          ph={4}
          phMd={4}
          phSm={4}
          pv={5}
          width={"50%"}
          widthMd={"100%"}
        >
          <Title
            color={tones[tone].titleColor}
            level={1}
            mb={3}
            size={size}
            sizeMd={sizeMd}
            sizeSm={sizeSm}
          >
            {title}
          </Title>
          <Text color={tones[tone].paragraphColor} size={"big"}>
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
              <AirsLink decoration={"none"} href={button1Link}>
                <Button
                  display={"block"}
                  onClick={matomoFreeTrialEvent}
                  variant={tones[tone].button1}
                >
                  {button1Text}
                </Button>
              </AirsLink>
            </Container>
            <Container ph={3} phSm={0} pv={1} width={"auto"} widthSm={"100%"}>
              <AirsLink href={button2Link}>
                <Button display={"block"} variant={tones[tone].button2}>
                  {button2Text}
                </Button>
              </AirsLink>
            </Container>
          </Container>
        </Container>
        <Container
          display={"flex"}
          justify={"end"}
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
