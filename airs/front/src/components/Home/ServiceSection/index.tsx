/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
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

import { NewRegularRedButton } from "../../../styles/styledComponents";
import { useCarrousel } from "../../../utils/hooks";
import { CloudImage } from "../../CloudImage";
import { Title } from "../../Texts";

const ServiceSection: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const timePerProgress = 100;
  const numberOfCycles = 6;
  const { cycle, progress } = useCarrousel(timePerProgress, numberOfCycles);

  return (
    <Container>
      <MainTextContainer>
        <Title fColor={"#fff"} fSize={"48"}>
          {t("service.homeTitle")}
        </Title>
        <ServiceParagraph>{t("service.homeParagraph")}</ServiceParagraph>
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
            <ProgressBar width={`${progress}%`} />
          </ProgressContainer>
          <div className={"tc-m"}>
            <Link
              className={"no-underline"}
              to={"/services/continuous-hacking/"}
            >
              <NewRegularRedButton className={"mv4 w-auto-ns w-100"}>
                {t("service.homeReadMore")}
              </NewRegularRedButton>
            </Link>
          </div>
        </CycleTextContainer>
      </CycleContainer>
    </Container>
  );
};

export { ServiceSection };
