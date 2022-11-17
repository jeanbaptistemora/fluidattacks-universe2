/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint react/forbid-component-props: 0 */
/* eslint fp/no-mutation:0 */
/* eslint react/jsx-no-bind:0 */
import React, { useEffect, useRef, useState } from "react";
import { IoIosArrowBack, IoIosArrowForward } from "react-icons/io";

import { SlideContainer } from "./styledComponents";
import type { ICardSlideShowProps } from "./types";

import { Button } from "../Button";
import { Container } from "../Container";
import { Text, Title } from "../Typography";
import { VerticalCard } from "../VerticalCard";

const CardSlideShow: React.FC<ICardSlideShowProps> = ({
  btnText,
  containerDescription,
  containerTitle,
  data,
}): JSX.Element => {
  const cards = data;
  const cardWidth = 360;
  const maxScroll = cardWidth * cards.length;
  const [currentWidth, setCurrentWidth] = useState(0);
  const [scroll, setScroll] = useState(0);

  const slideDiv = useRef<HTMLDivElement>(null);

  const scrollLeft: () => void = (): void => {
    setScroll(scroll < cardWidth ? 0 : scroll - cardWidth);
  };

  const scrollRight: () => void = (): void => {
    setScroll(
      scroll > currentWidth - cardWidth ? currentWidth : scroll + cardWidth
    );
  };

  const changeScroll: (element: React.RefObject<HTMLDivElement>) => void = (
    element
  ): void => {
    if (element.current) {
      if (
        element.current.scrollLeft > 0 ||
        element.current.scrollLeft < currentWidth
      ) {
        element.current.scrollLeft = scroll;
      } else {
        element.current.scrollLeft += 0;
      }
      setCurrentWidth(maxScroll - element.current.offsetWidth);
    }
  };

  useEffect((): void => {
    changeScroll(slideDiv);
  });

  return (
    <Container bgColor={"#25252d"} ph={4} pv={5}>
      <Container center={true} mb={3} width={"1237px"}>
        <Title
          color={"#fff"}
          level={2}
          mb={1}
          size={"medium"}
          textAlign={"center"}
        >
          {containerTitle}
        </Title>
        <Text color={"#b0b0bf"} size={"big"} textAlign={"center"}>
          {containerDescription}
        </Text>
      </Container>
      <SlideContainer>
        <Container>
          <Button icon={<IoIosArrowBack />} onClick={scrollLeft} />
          <Button icon={<IoIosArrowForward />} onClick={scrollRight} />
        </Container>
        <div className={"flex overflow-hidden scroll-smooth"} ref={slideDiv}>
          {cards.map((card): JSX.Element => {
            const { alt, description, image, title, slug } =
              card.node.frontmatter;

            return (
              <VerticalCard
                alt={alt}
                btnText={btnText}
                description={description}
                image={image}
                key={title}
                link={slug}
                minWidth={"344px"}
                title={title}
                titleMinHeight={"80px"}
                width={"344px"}
              />
            );
          })}
        </div>
      </SlideContainer>
    </Container>
  );
};

export { CardSlideShow };
