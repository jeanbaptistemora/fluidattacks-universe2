/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
  const slideDiv = useRef<HTMLDivElement>(null);
  const cardDiv = useRef<HTMLDivElement>(null);

  const [cardWidth, setCardWidth] = useState(0);
  const [currentWidth, setCurrentWidth] = useState(0);
  const [scroll, setScroll] = useState(0);

  const cards = data;
  const maxScroll = cardWidth * cards.length;

  const scrollLeft: () => void = (): void => {
    setScroll(scroll < cardWidth ? 0 : scroll - cardWidth);
  };

  const scrollRight: () => void = (): void => {
    setScroll(
      scroll > currentWidth - cardWidth ? currentWidth : scroll + cardWidth
    );
  };

  useEffect((): void => {
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

    setCardWidth(cardDiv.current ? cardDiv.current.offsetWidth : 0);
    changeScroll(slideDiv);
  }, [currentWidth, maxScroll, scroll]);

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
        <div className={"flex overflow-hidden scroll-smooth"} ref={slideDiv}>
          {cards.map((card): JSX.Element => {
            const { alt, description, image, title } = card.node.frontmatter;
            const { slug } = card.node.fields;

            return (
              <div className={"flex"} key={title} ref={cardDiv}>
                <VerticalCard
                  alt={alt}
                  btnText={btnText}
                  description={description}
                  image={image}
                  link={slug}
                  minWidth={"344px"}
                  minWidthSm={"270px"}
                  title={title}
                  titleMinHeight={"80px"}
                />
              </div>
            );
          })}
        </div>
        <Container display={"flex"} mh={2} mt={3}>
          <Container mr={2} width={"auto"}>
            <Button
              disabled={scroll === 0}
              icon={<IoIosArrowBack />}
              onClick={scrollLeft}
              size={"lg"}
              variant={"darkSecondary"}
            />
          </Container>
          <Container width={"auto"}>
            <Button
              disabled={scroll === currentWidth}
              icon={<IoIosArrowForward />}
              onClick={scrollRight}
              size={"lg"}
              variant={"darkSecondary"}
            />
          </Container>
        </Container>
      </SlideContainer>
    </Container>
  );
};

export { CardSlideShow };
