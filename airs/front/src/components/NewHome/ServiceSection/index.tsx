/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import {
  Container,
  CycleContainer,
  CycleControl,
  CycleImageContainer,
  CycleParagraph,
  CycleTextContainer,
  CycleTitle,
  MainTextContainer,
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
  const changeCycle = useCallback((index: number): (() => void) => {
    return (): void => {
      setCycle(index);
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
          {Array(numberOfCycles)
            .fill(undefined)
            .map((_, index): JSX.Element => {
              return (
                <CycleControl
                  active={index === cycle}
                  key={`${t(`service.cycleTitle${index}`)}`}
                  onClick={changeCycle(index)}
                />
              );
            })}
        </CycleTextContainer>
      </CycleContainer>
    </Container>
  );
};

export { ServiceSection };
