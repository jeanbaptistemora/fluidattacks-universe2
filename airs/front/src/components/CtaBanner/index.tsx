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
  image,
  matomoAction,
  paragraph,
  title,
}): JSX.Element => {
  const { trackEvent } = useMatomo();

  const matomoFreeTrialEvent = (): void => {
    trackEvent({
      action: "cta-free-trial-event-click",
      category: `${matomoAction}`,
    });
  };

  return (
    <Container
      align={"center"}
      bgColor={"#f4f4f6"}
      br={4}
      center={true}
      display={"flex"}
      justify={"center"}
      maxWidth={"1440px"}
      shadow={true}
      wrap={"wrap"}
    >
      <Container ph={4} pv={5} width={"70%"} widthMd={"100%"}>
        <Title color={"#2e2e38"} level={1} mb={3} size={"big"}>
          {title}
        </Title>
        <Text color={"#65657b"} size={"big"}>
          {paragraph}
        </Text>
        <Container display={"flex"} mv={3} wrap={"wrap"}>
          <Container ph={1} pv={1} width={"auto"} widthMd={"100%"}>
            <AirsLink href={"/free-trial/"}>
              <Button
                display={"block"}
                onClick={matomoFreeTrialEvent}
                variant={"primary"}
              >
                {"Start free trial"}
              </Button>
            </AirsLink>
          </Container>
          <Container ph={1} pv={1} width={"auto"} widthMd={"100%"}>
            <AirsLink href={"/contact-us/"}>
              <Button display={"block"} variant={"tertiary"}>
                {"Contact now"}
              </Button>
            </AirsLink>
          </Container>
        </Container>
      </Container>
      <Container
        display={"flex"}
        justify={"end"}
        width={"30%"}
        widthMd={"100%"}
      >
        <CloudImage alt={title} src={image} />
      </Container>
    </Container>
  );
};

export { CtaBanner };
