/* eslint react/jsx-no-bind:0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import React, { useCallback } from "react";

import type { ICtaBannerProps, IVariant, TVariant } from "./types";

import { useWindowSize } from "../../utils/hooks/useWindowSize";
import { AirsLink } from "../AirsLink";
import { Button } from "../Button";
import { CloudImage } from "../CloudImage";
import { Container } from "../Container";
import { Text, Title } from "../Typography";

const CtaBanner: React.FC<ICtaBannerProps> = ({
  button1Link,
  button1Text,
  button2Link,
  button2Text,
  image,
  matomoAction,
  maxWidth,
  paragraph,
  pv = 5,
  pvMd = 5,
  pvSm = 5,
  size = "big",
  sizeMd,
  sizeSm,
  textSize = "big",
  title,
  variant = "light",
}): JSX.Element => {
  const { trackEvent } = useMatomo();
  const { width } = useWindowSize();
  const alignTextHook = width > 960 ? "start" : "center";

  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({
      action: "cta-banner-click",
      category: `${matomoAction}`,
    });
  }, [matomoAction, trackEvent]);

  const variants: Record<TVariant, IVariant> = {
    dark: {
      bgColor: "#2e2e38",
      color: "#fff",
      subColor: "#dddde3",
    },
    light: {
      bgColor: "#f4f4f6",
      color: "#2e2e38",
      subColor: "#65657b",
    },
  };

  if (
    image !== undefined &&
    button2Link !== undefined &&
    paragraph !== undefined
  ) {
    return (
      <Container
        align={"center"}
        bgColor={variants[variant].bgColor}
        br={4}
        center={true}
        display={"flex"}
        justify={"center"}
        maxWidth={maxWidth === undefined ? "1440px" : maxWidth}
        ph={4}
        pv={pv}
        pvMd={pvMd}
        pvSm={pvSm}
        shadow={true}
        wrap={"wrap"}
      >
        <Container width={"60%"} widthMd={"100%"}>
          <Title
            color={variants[variant].color}
            level={2}
            mb={3}
            size={size}
            sizeMd={sizeMd}
            sizeSm={sizeSm}
            textAlign={alignTextHook}
          >
            {title}
          </Title>
          <Text
            color={variants[variant].subColor}
            size={textSize}
            textAlign={alignTextHook}
          >
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
                  variant={"primary"}
                >
                  <Text color={"inherit"}>{button1Text}</Text>
                </Button>
              </AirsLink>
            </Container>
            <Container ph={3} phSm={0} pv={1} width={"auto"} widthSm={"100%"}>
              <AirsLink decoration={"none"} href={button2Link}>
                <Button
                  display={"block"}
                  variant={variant === "light" ? "tertiary" : "darkTertiary"}
                >
                  <Text color={"inherit"}>{button2Text}</Text>
                </Button>
              </AirsLink>
            </Container>
          </Container>
        </Container>
        <Container
          display={"flex"}
          justify={"center"}
          width={"40%"}
          widthMd={"100%"}
        >
          <CloudImage alt={title} src={image} />
        </Container>
      </Container>
    );
  } else if (button2Link !== undefined && paragraph !== undefined) {
    return (
      <Container
        align={"center"}
        bgColor={variants[variant].bgColor}
        br={4}
        center={true}
        maxWidth={maxWidth === undefined ? "1440px" : maxWidth}
        ph={4}
        pv={pv}
        shadow={true}
      >
        <Title
          color={variants[variant].color}
          level={2}
          mb={3}
          size={size}
          sizeMd={sizeMd}
          sizeSm={sizeSm}
          textAlign={"center"}
        >
          {title}
        </Title>
        <Text
          color={variants[variant].subColor}
          size={textSize}
          textAlign={"center"}
        >
          {paragraph}
        </Text>
        <Container display={"flex"} justify={"center"} mt={3} wrap={"wrap"}>
          <Container pv={1} width={"auto"} widthSm={"100%"}>
            <AirsLink decoration={"none"} href={button1Link}>
              <Button
                display={"block"}
                onClick={matomoFreeTrialEvent}
                variant={"primary"}
              >
                <Text color={"inherit"}>{button1Text}</Text>
              </Button>
            </AirsLink>
          </Container>
          <Container ph={3} phSm={0} pv={1} width={"auto"} widthSm={"100%"}>
            <AirsLink decoration={"none"} href={button2Link}>
              <Button display={"block"} variant={"tertiary"}>
                <Text color={"inherit"}>{button2Text}</Text>
              </Button>
            </AirsLink>
          </Container>
        </Container>
      </Container>
    );
  } else if (paragraph !== undefined) {
    return (
      <Container
        align={"center"}
        bgColor={variants[variant].bgColor}
        br={4}
        center={true}
        display={"flex"}
        justify={"center"}
        maxWidth={maxWidth === undefined ? "1440px" : maxWidth}
        ph={4}
        pv={pv}
        shadow={true}
        wrap={"wrap"}
      >
        <Container width={"70%"} widthMd={"100%"}>
          <Title
            color={variants[variant].color}
            level={2}
            size={size}
            sizeMd={sizeMd}
            sizeSm={sizeSm}
          >
            {title}
          </Title>
          <Text color={variants[variant].subColor} mt={3} size={textSize}>
            {paragraph}
          </Text>
        </Container>
        <Container
          display={"flex"}
          justify={"center"}
          width={"30%"}
          widthMd={"100%"}
        >
          <Container mtMd={3} width={"auto"} widthSm={"100%"}>
            <AirsLink decoration={"none"} href={button1Link}>
              <Button
                display={"block"}
                onClick={matomoFreeTrialEvent}
                size={"lg"}
                variant={"primary"}
              >
                <Text color={"inherit"}>{button1Text}</Text>
              </Button>
            </AirsLink>
          </Container>
        </Container>
      </Container>
    );
  }

  return (
    <Container
      align={"center"}
      bgColor={variants[variant].bgColor}
      br={4}
      center={true}
      display={"flex"}
      justify={"center"}
      maxWidth={maxWidth === undefined ? "1440px" : maxWidth}
      ph={4}
      pv={pv}
      shadow={true}
      wrap={"wrap"}
    >
      <Container width={"70%"} widthMd={"100%"}>
        <Title
          color={variants[variant].color}
          level={2}
          size={size}
          sizeMd={sizeMd}
          sizeSm={sizeSm}
        >
          {title}
        </Title>
      </Container>
      <Container
        display={"flex"}
        justify={"center"}
        width={"30%"}
        widthMd={"100%"}
      >
        <Container mtMd={3} width={"auto"} widthSm={"100%"}>
          <AirsLink decoration={"none"} href={button1Link}>
            <Button
              display={"block"}
              onClick={matomoFreeTrialEvent}
              size={"lg"}
              variant={"primary"}
            >
              <Text color={"inherit"}>{button1Text}</Text>
            </Button>
          </AirsLink>
        </Container>
      </Container>
    </Container>
  );
};

export { CtaBanner };
