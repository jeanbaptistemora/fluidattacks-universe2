/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import {
  CardContainer,
  Container,
  ImageContainer,
  PortraitContainer,
} from "./styledComponents";

import {
  FlexCenterItemsContainer,
  NewRegularRedButton,
  PhantomRegularRedButton,
} from "../../../styles/styledComponents";
import { translate } from "../../../utils/translations/translate";
import { CloudImage } from "../../CloudImage";
import { Paragraph, Title } from "../../Texts";

const Portrait: React.FC = (): JSX.Element => {
  return (
    <Container>
      <PortraitContainer>
        <ImageContainer>
          <CloudImage
            alt={"plans-portrait"}
            src={"/airs/plans/plans-cta"}
            styles={"w-100 h-100"}
          />
        </ImageContainer>
        <CardContainer>
          <Title fColor={"#2e2e38"} fSize={"48"} fSizeS={"34"}>
            {translate.t("plansPage.portrait.title")}
          </Title>
          <Paragraph
            fColor={"#5c5c70"}
            fSize={"24"}
            marginBottom={"2"}
            marginTop={"1"}
            maxWidth={"1000"}
          >
            {translate.t("plansPage.portrait.paragraph")}
          </Paragraph>
          <FlexCenterItemsContainer className={"flex-wrap"}>
            <Link to={"/free-trial/"}>
              <NewRegularRedButton className={"mh2 mv3"}>
                {"Start free trial"}
              </NewRegularRedButton>
            </Link>
            <Link to={"/contact-us-demo/"}>
              <PhantomRegularRedButton className={"mh2"}>
                {"Request a demo"}
              </PhantomRegularRedButton>
            </Link>
          </FlexCenterItemsContainer>
        </CardContainer>
      </PortraitContainer>
    </Container>
  );
};

export { Portrait };
