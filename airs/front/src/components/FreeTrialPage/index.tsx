/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
import React from "react";

import {
  BlackContainer,
  Container,
  ImageContainer,
  InternalContainer,
  WhiteContainer,
} from "./styledComponents";

import { NewRegularRedButton } from "../../styles/styledComponents";
import { translate } from "../../utils/translations/translate";
import { AirsLink } from "../AirsLink";
import { CloudImage } from "../CloudImage";
import { Paragraph, Title } from "../Texts";

const FreeTrialPage: React.FC = (): JSX.Element => {
  const items = [
    { text: translate.t("freeTrial.item1") },
    { text: translate.t("freeTrial.item2") },
    { text: translate.t("freeTrial.item3") },
    { text: translate.t("freeTrial.item4") },
    { text: translate.t("freeTrial.item5") },
  ];

  return (
    <Container>
      <WhiteContainer>
        <ImageContainer>
          <CloudImage
            alt={"Fluid Logo"}
            src={"airs/logo_fluid_attacks_2021_eqop3k"}
          />
        </ImageContainer>
        <InternalContainer>
          <Title
            fColor={"#2e2e38"}
            fSize={"32"}
            marginBottom={"1.5"}
            maxWidth={"450"}
          >
            {translate.t("freeTrial.title")}
          </Title>
          <Paragraph fColor={"#5c5c70"} fSize={"24"} marginBottom={"1.5"}>
            {translate.t("freeTrial.subtitle")}
          </Paragraph>
          <ul>
            {items.map((item): JSX.Element => {
              return (
                <li key={item.text}>
                  <Paragraph fColor={"#5c5c70"} fSize={"16"}>
                    {item.text}
                  </Paragraph>
                </li>
              );
            })}
          </ul>
          <AirsLink href={"https://app.fluidattacks.com/#trial"}>
            <NewRegularRedButton>
              {translate.t("freeTrial.button")}
            </NewRegularRedButton>
          </AirsLink>
        </InternalContainer>
      </WhiteContainer>
      <BlackContainer>
        <InternalContainer>
          <CloudImage alt={"Portrait"} src={"/airs/home/portrait-home"} />
        </InternalContainer>
      </BlackContainer>
    </Container>
  );
};

export { FreeTrialPage };
