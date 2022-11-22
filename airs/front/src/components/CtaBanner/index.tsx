/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint react/jsx-no-bind:0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import React from "react";

import type { ICtaBannerProps } from "./types";

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
  paragraph,
  size = "big",
  sizeMd,
  sizeSm,
  title,
}): JSX.Element => {
  const { trackEvent } = useMatomo();

  const matomoFreeTrialEvent = (): void => {
    trackEvent({
      action: "cta-banner-click",
      category: `${matomoAction}`,
    });
  };

  if (image !== undefined) {
    return (
      <Container
        align={"center"}
        bgColor={"#f4f4f6"}
        br={4}
        center={true}
        display={"flex"}
        justify={"center"}
        maxWidth={"1440px"}
        ph={4}
        pv={5}
        shadow={true}
        wrap={"wrap"}
      >
        <Container width={"60%"} widthMd={"100%"}>
          <Title
            color={"#2e2e38"}
            level={2}
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
          width={"40%"}
          widthMd={"100%"}
        >
          <CloudImage alt={title} src={image} />
        </Container>
      </Container>
    );
  }

  return (
    <Container
      align={"center"}
      bgColor={"#f4f4f6"}
      br={4}
      center={true}
      maxWidth={"1440px"}
      ph={4}
      pv={5}
      shadow={true}
    >
      <Title
        color={"#2e2e38"}
        level={2}
        mb={3}
        size={size}
        sizeMd={sizeMd}
        sizeSm={sizeSm}
        textAlign={"center"}
      >
        {title}
      </Title>
      <Text color={"#65657b"} size={"big"} textAlign={"center"}>
        {paragraph}
      </Text>
      <Container display={"flex"} justify={"center"} mv={3} wrap={"wrap"}>
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
  );
};

export { CtaBanner };
