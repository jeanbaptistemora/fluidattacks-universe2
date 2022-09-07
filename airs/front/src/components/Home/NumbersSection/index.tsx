/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";
import { useTranslation } from "react-i18next";

import { Carousel } from "./Carousel";
import { Grid } from "./Grid";
import { Container, TitleContainer } from "./styledComponents";

import { useCarrousel } from "../../../utils/hooks";
import { Title } from "../../Texts";

const NumbersSection: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const data = [
    {
      hasTitle: true,
      image: "card-1",
      isGray: true,
      text: t("numbersSection.card1Description"),
      title: t("numbersSection.card1Title"),
      typeIcon: "1",
    },
    {
      hasTitle: true,
      image: "card-2",
      isGray: true,
      text: t("numbersSection.card2Description"),
      title: t("numbersSection.card2Title"),
      typeIcon: "1",
    },
    {
      hasTitle: true,
      image: "card-3",
      isGray: true,
      text: t("numbersSection.card3Description"),
      title: t("numbersSection.card3Title"),
      typeIcon: "1",
    },
    {
      hasTitle: true,
      image: "card-4",
      isGray: true,
      text: t("numbersSection.card4Description"),
      title: t("numbersSection.card4Title"),
      typeIcon: "1",
    },
    {
      hasTitle: true,
      image: "card-5",
      isGray: true,
      text: t("numbersSection.card5Description"),
      title: t("numbersSection.card5Title"),
      typeIcon: "1",
    },
    {
      hasTitle: true,
      image: "card-6",
      isGray: true,
      text: t("numbersSection.card6Description"),
      title: t("numbersSection.card6Title"),
      typeIcon: "2",
    },
    {
      hasTitle: true,
      image: "card-7",
      isGray: true,
      text: t("numbersSection.card7Description"),
      title: t("numbersSection.card7Title"),
      typeIcon: "2",
    },
    {
      hasTitle: true,
      image: "card-8",
      isGray: true,
      text: t("numbersSection.card8Description"),
      title: t("numbersSection.card8Title"),
      typeIcon: "1",
    },
  ];

  const timePerProgress = 100;
  const { cycle, progress } = useCarrousel(timePerProgress, data.length);

  return (
    <Container>
      <TitleContainer>
        <Title fColor={"#fff"} fSize={"48"}>
          {t("numbersSection.title")}
        </Title>
      </TitleContainer>
      <Grid data={data} />
      <Carousel data={data[cycle]} progressValue={progress} />
    </Container>
  );
};

export { NumbersSection };
