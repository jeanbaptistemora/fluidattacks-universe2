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
  title,
  paragraph,
  image,
}): JSX.Element => {
  const { trackEvent } = useMatomo();

  const matomoFreeTrialEvent = (): void => {
    trackEvent({
      action: "cta-free-trial-event-click",
      category: "solutions",
    });
  };

  return (
    <Container bgColor={"#ffffff"}>
      <Container
        bgColor={"#f4f4f6"}
        borderColor={"#dddde3"}
        br={4}
        center={true}
        display={"flex"}
        height={"90%"}
        maxWidth={"1500px"}
        pl={3}
        width={"95%"}
        wrap={"wrap"}
      >
        <Container
          display={"flex"}
          maxWidth={"800px"}
          pv={5}
          width={"50%"}
          widthMd={"100%"}
          widthSm={"100%"}
          wrap={"wrap"}
        >
          <Title color={"#2e2e38"} level={1} mb={4} size={"big"}>
            {title}
          </Title>
          <Text color={"#65657b"} size={"big"}>
            {paragraph}
          </Text>
          <Container display={"flex"} pt={3} widthSm={"100%"} wrap={"wrap"}>
            <Container pb={3} pr={1} width={"200px"} widthSm={"100%"}>
              <AirsLink href={"/free-trial/"}>
                <Button
                  display={"block"}
                  onClick={matomoFreeTrialEvent}
                  size={"lg"}
                  variant={"primary"}
                >
                  {"Start free trial"}
                </Button>
              </AirsLink>
            </Container>
            <Container pb={5} width={"200px"} widthSm={"100%"}>
              <AirsLink href={"/contact-us/"}>
                <Button display={"block"} size={"lg"} variant={"tertiary"}>
                  {"Contact now"}
                </Button>
              </AirsLink>
            </Container>
          </Container>
        </Container>
        <Container
          display={"flex"}
          justify={"end"}
          width={"50%"}
          widthMd={"0%"}
          widthSm={"0%"}
        >
          <CloudImage alt={title} src={image} />
        </Container>
      </Container>
    </Container>
  );
};

export { CtaBanner };
