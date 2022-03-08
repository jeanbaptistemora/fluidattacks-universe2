/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import {
  Container,
  CycleContainer,
  CycleImageContainer,
  CycleParagraph,
  CycleTextContainer,
  CycleTitle,
  MainTextContainer,
  ProgressBar,
  ProgressContainer,
  ServiceParagraph,
} from "./styledComponents";

import {
  NewRegularRedButton,
  WhiteBigParagraph,
} from "../../../styles/styledComponents";
import { CloudImage } from "../../CloudImage";

const ServiceSection: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const [cycle, setCycle] = useState(0);
  const numberOfCycles = 6;
  const timePerProgress = 100;
  const progressLimit = 100;
  const [progressValue, setprogressValue] = useState(0);

  useEffect((): (() => void) => {
    const changeCycle = (): void => {
      setCycle((currentIndex): number =>
        currentIndex === numberOfCycles - 1 ? 0 : currentIndex + 1
      );
    };

    const changeprogressValue = (): void => {
      setprogressValue((currentTime): number => {
        if (currentTime === progressLimit) {
          changeCycle();
        }

        return currentTime === progressLimit ? 0 : currentTime + 1;
      });
    };

    const timer = setInterval(changeprogressValue, timePerProgress);

    return (): void => {
      clearInterval(timer);
    };
  }, []);

  return (
    <Container>
      <MainTextContainer>
        <WhiteBigParagraph>{t("service.homeTitle")}</WhiteBigParagraph>
        <ServiceParagraph>{t("service.homeParagraph")}</ServiceParagraph>
        <Link className={"no-underline"} to={"/newHome"}>
          <NewRegularRedButton className={"mv4 w-auto-ns w-100"}>
            {t("service.homeReadMore")}
          </NewRegularRedButton>
        </Link>
      </MainTextContainer>
      <CycleContainer>
        <CycleImageContainer>
          <CloudImage
            alt={"service-cycle"}
            src={`airs/home/cycle-${cycle}`}
            styles={"cycle-img w-100 h-100 fr-l"}
          />
        </CycleImageContainer>
        <CycleTextContainer>
          <CycleTitle>{t(`service.cycleTitle${cycle}`)}</CycleTitle>
          <CycleParagraph>{t(`service.cycleParagraph${cycle}`)}</CycleParagraph>
          <ProgressContainer>
            <ProgressBar width={`${progressValue}%`} />
          </ProgressContainer>
        </CycleTextContainer>
      </CycleContainer>
    </Container>
  );
};

export { ServiceSection };
