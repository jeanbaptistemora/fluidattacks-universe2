import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import Media from "react-media";

import { Carousel } from "./Carousel";
import { Grid } from "./Grid";
import { Container, TitleContainer } from "./styledComponents";

import { WhiteBigParagraph } from "../../../styles/styledComponents";

const NumbersSection: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const data = [
    {
      hasTitle: false,
      image: "card-1",
      isGray: false,
      text: t("numbersSection.card1Description"),
      typeIcon: "1",
    },
    {
      hasTitle: false,
      image: "card-2",
      isGray: false,
      text: t("numbersSection.card2Description"),
      typeIcon: "1",
    },
    {
      hasTitle: false,
      image: "card-3",
      isGray: false,
      text: t("numbersSection.card3Description"),
      typeIcon: "1",
    },
    {
      hasTitle: false,
      image: "card-4",
      isGray: false,
      text: t("numbersSection.card4Description"),
      typeIcon: "1",
    },
    {
      hasTitle: false,
      image: "card-5",
      isGray: false,
      text: t("numbersSection.card5Description"),
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
  const progressLimit = 100;
  const timePerCard = 5000;
  const [cardIndex, setCardIndex] = useState(0);
  const progressValue = (cardIndex / (data.length - 1)) * progressLimit;

  useEffect((): void => {
    const changeCardIndex = (): void => {
      setCardIndex((currentIndex): number =>
        currentIndex === data.length - 1 ? 0 : currentIndex + 1
      );
    };

    setInterval(changeCardIndex, timePerCard);
  }, [data.length]);

  return (
    <Container>
      <TitleContainer>
        <WhiteBigParagraph>{t("numbersSection.title")}</WhiteBigParagraph>
      </TitleContainer>
      <Media query={{ minWidth: 960 }}>
        {(matches): JSX.Element =>
          matches ? (
            <Grid data={data} />
          ) : (
            <Carousel data={data[cardIndex]} progressValue={progressValue} />
          )
        }
      </Media>
    </Container>
  );
};

export { NumbersSection };
