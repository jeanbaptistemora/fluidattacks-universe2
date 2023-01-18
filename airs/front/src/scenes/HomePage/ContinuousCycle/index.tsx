/* eslint fp/no-mutation:0 */
import React, { useCallback, useEffect, useState } from "react";
import {
  BsFillArrowLeftCircleFill,
  BsFillArrowRightCircleFill,
} from "react-icons/bs";

import { ProgressBar, SlideHook, SlideShow } from "./styledComponents";

import { Button } from "../../../components/Button";
import { CloudImage } from "../../../components/CloudImage";
import { Container } from "../../../components/Container";
import { Grid } from "../../../components/Grid";
import { Text, Title } from "../../../components/Typography";
import { useCarrousel } from "../../../utils/hooks";
import { useWindowSize } from "../../../utils/hooks/useWindowSize";
import { translate } from "../../../utils/translations/translate";

const ContinuousCycle: React.FC = (): JSX.Element => {
  const { width } = useWindowSize();
  const [state, setState] = useState(0);
  const screen = width > 960 ? "big" : "md";

  const timePerProgress = 50;
  const numberOfCycles = 6;
  const { cycle, progress } = useCarrousel(timePerProgress, numberOfCycles);

  const cardWidth = width * 0.63;
  const maxScroll = cardWidth * 7;

  const [currentWidth, setCurrentWidth] = useState(0);
  const [scroll, setScroll] = useState(0);
  const scrollLeft: () => void = useCallback((): void => {
    setState(state - 1);
    setScroll(scroll < cardWidth ? 0 : scroll - cardWidth);
  }, [cardWidth, state, scroll]);
  const getProgress = useCallback(
    (el: number): string => {
      if (cycle > el) {
        return "100%";
      }

      return cycle === el ? `${progress}%` : "0%";
    },
    [cycle, progress]
  );

  const scrollRight: () => void = useCallback((): void => {
    setState(state + 1);
    setScroll(
      scroll > currentWidth - cardWidth ? currentWidth : scroll + cardWidth
    );
  }, [scroll, currentWidth, cardWidth, state]);

  const changeScroll: (element: HTMLElement) => void = (
    element: HTMLElement
  ): void => {
    if (element.scrollLeft > 0 || element.scrollLeft < currentWidth) {
      element.scrollLeft = scroll;
    } else {
      element.scrollLeft += 0;
    }
    setCurrentWidth(maxScroll - element.offsetWidth);
  };

  useEffect((): void => {
    const slideShow: HTMLElement = document.getElementById(
      "solutionsSlides"
    ) as HTMLElement;
    changeScroll(slideShow);
  });

  if (screen === "md") {
    return (
      <Container bgColor={"#ffffff"}>
        <Container display={"flex"} justify={"end"}>
          <Container
            align={"center"}
            display={"flex"}
            justify={"end"}
            maxWidth={"1420px"}
            mr={0}
            wrap={"wrap"}
          >
            <Container ph={4} pv={5} width={"70%"} widthMd={"100%"}>
              <Title color={"#bf0b1a"} level={3} mb={3} size={"small"}>
                {translate.t("home.continuousCycle.subtitle")}
              </Title>
              <Title color={"#11111"} level={1} size={"medium"}>
                {translate.t("home.continuousCycle.title")}
              </Title>
            </Container>
            <div style={{ width: "30%" }} />
          </Container>
        </Container>
        <Grid columns={1} columnsMd={1} columnsSm={1} gap={"7rem"}>
          <Container
            align={"center"}
            center={true}
            display={"flex"}
            justify={"center"}
          >
            <Container maxWidth={"80%"}>
              <CloudImage
                alt={"cycle-image"}
                src={`airs/home/ContinuousCycle/ciclo-hc-fluid-${state}.png`}
              />
            </Container>
          </Container>
          <SlideShow id={"solutionsSlides"}>
            {[...Array(6).keys()].map(
              (el: number): JSX.Element => (
                <Container
                  bgColor={"#ffffff"}
                  hoverColor={"#f4f4f6"}
                  key={`cycle${el}`}
                  maxWidth={"97%"}
                  minHeight={"100px"}
                  minWidth={"70%"}
                  pr={state === 5 ? 1 : 0}
                  topBar={state >= el ? "#bf0b1a" : "#ffffff"}
                >
                  <Container pl={3}>
                    <Title color={"#2e2e38"} level={4} size={"small"}>
                      {translate.t(`home.continuousCycle.cycle${el}.title`)}
                    </Title>
                    <Text color={"#535365"}>
                      {translate.t(`home.continuousCycle.cycle${el}.subtitle`)}
                    </Text>
                  </Container>
                </Container>
              )
            )}
          </SlideShow>
        </Grid>
        <Container display={"flex"} justify={"center"} pb={2} wrap={"wrap"}>
          <Button disabled={state === 0} onClick={scrollLeft} size={"lg"}>
            <BsFillArrowLeftCircleFill color={"#40404f"} size={50} />
          </Button>
          <Button disabled={state === 5} onClick={scrollRight}>
            <BsFillArrowRightCircleFill color={"#40404f"} size={50} />
          </Button>
        </Container>
      </Container>
    );
  }

  return (
    <Container bgColor={"#ffffff"} ph={6} pv={5}>
      <Container display={"flex"} justify={"end"}>
        <Container
          align={"center"}
          display={"flex"}
          justify={"end"}
          maxWidth={"1420px"}
          mr={0}
          wrap={"wrap"}
        >
          <Container pv={5} width={"70%"} widthMd={"100%"}>
            <Title color={"#bf0b1a"} level={3} mb={3} size={"small"}>
              {translate.t("home.continuousCycle.subtitle")}
            </Title>
            <Title color={"#11111"} level={1} size={"medium"}>
              {translate.t("home.continuousCycle.title")}
            </Title>
          </Container>
          <div style={{ width: "30%" }} />
        </Container>
      </Container>
      <Grid columns={2} columnsMd={1} columnsSm={1} gap={"7rem"}>
        <Container display={"flex"} justify={"end"} wrap={"wrap"}>
          {[...Array(6).keys()].map(
            (el: number): JSX.Element => (
              <Container
                bgColor={"#ffffff"}
                display={"flex"}
                height={"153px"}
                key={`cycle${el}`}
                maxWidth={"555px"}
                wrap={"wrap"}
              >
                <Container bgColor={"#DDDDE3"} width={"5px"}>
                  <ProgressBar width={getProgress(el)} />
                </Container>
                <SlideHook id={"solutionsSlides"} />
                <Container maxWidth={"90%"} pl={3} pt={2}>
                  <Title color={"#2e2e38"} level={4} size={"small"}>
                    {translate.t(`home.continuousCycle.cycle${el}.title`)}
                  </Title>
                  <Text color={"#535365"}>
                    {translate.t(`home.continuousCycle.cycle${el}.subtitle`)}
                  </Text>
                </Container>
              </Container>
            )
          )}
        </Container>
        <Container
          align={"center"}
          center={true}
          display={"flex"}
          justify={"center"}
        >
          <Container>
            <CloudImage
              alt={"cycle-image"}
              src={`airs/home/ContinuousCycle/ciclo-hc-fluid-${cycle}.png`}
            />
          </Container>
        </Container>
      </Grid>
    </Container>
  );
};

export { ContinuousCycle };
