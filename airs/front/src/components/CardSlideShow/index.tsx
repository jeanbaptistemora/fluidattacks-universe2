/* eslint fp/no-mutation:0 */
/* eslint react/jsx-no-bind:0 */
import React, { useCallback, useEffect, useRef, useState } from "react";
import { IoIosArrowBack, IoIosArrowForward } from "react-icons/io";

import { SlideContainer } from "./styledComponents";
import type { ICardSlideShowProps, IVariant, TVariant } from "./types";

import { Button } from "../Button";
import { Container } from "../Container";
import { Text, Title } from "../Typography";
import { VerticalCard } from "../VerticalCard";

const CardSlideShow: React.FC<ICardSlideShowProps> = ({
  btnText,
  containerDescription,
  containerTitle,
  data,
  variant = "light",
}): JSX.Element => {
  const variants: Record<TVariant, IVariant> = {
    dark: {
      bgColor: "#25252d",
      button: "darkSecondary",
      subtitleColor: "#b0b0bf",
      titleColor: "#fff",
    },
    light: {
      bgColor: "#dddde3",
      button: "secondary",
      subtitleColor: "#535365",
      titleColor: "#25252d",
    },
  };

  const slideDiv = useRef<HTMLDivElement>(null);
  const cardDiv = useRef<HTMLDivElement>(null);

  const [cardWidth, setCardWidth] = useState(0);
  const [currentWidth, setCurrentWidth] = useState(0);
  const [scroll, setScroll] = useState(0);

  const cards = data;
  const maxScroll = cardWidth * cards.length;

  const scrollLeft: () => void = useCallback((): void => {
    setScroll(scroll < cardWidth ? 0 : scroll - cardWidth);
  }, [cardWidth, scroll]);

  const scrollRight: () => void = useCallback((): void => {
    setScroll(
      scroll > currentWidth - cardWidth ? currentWidth : scroll + cardWidth
    );
  }, [cardWidth, currentWidth, scroll]);

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
    <Container bgColor={variants[variant].bgColor} ph={4} pv={5}>
      <Container center={true} mb={3} width={"1237px"}>
        <Title
          color={variants[variant].titleColor}
          level={2}
          mb={1}
          size={"medium"}
          textAlign={"center"}
        >
          {containerTitle}
        </Title>
        <Text
          color={variants[variant].subtitleColor}
          size={"big"}
          textAlign={"center"}
        >
          {containerDescription}
        </Text>
      </Container>
      <SlideContainer initialWidth={maxScroll > 1440 ? 1440 : maxScroll}>
        <div className={"flex overflow-hidden scroll-smooth"} ref={slideDiv}>
          {cards.map((card): JSX.Element => {
            const { alt, image, subtitle, title } = card.node.frontmatter;
            const { slug } = card.node.fields;

            return (
              <div className={"flex"} key={title} ref={cardDiv}>
                <VerticalCard
                  alt={alt}
                  btnText={btnText}
                  description={subtitle}
                  image={image}
                  link={slug}
                  mh={2}
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
              variant={variants[variant].button}
            />
          </Container>
          <Container width={"auto"}>
            <Button
              disabled={scroll === currentWidth}
              icon={<IoIosArrowForward />}
              onClick={scrollRight}
              size={"lg"}
              variant={variants[variant].button}
            />
          </Container>
        </Container>
      </SlideContainer>
    </Container>
  );
};

export { CardSlideShow };
