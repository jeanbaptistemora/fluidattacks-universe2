/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import {
  BlackContainer,
  Container,
  InternalContainer,
  WhiteContainer,
} from "./styledComponents";

import { NewRegularRedButton } from "../../styles/styledComponents";
import { translate } from "../../utils/translations/translate";
import { CloudImage } from "../CloudImage";
import { Paragraph, Title } from "../Texts";

const FreeTrialPage: React.FC = (): JSX.Element => {
  const items = [
    { text: translate.t("freeTrial.item1") },
    { text: translate.t("freeTrial.item2") },
    { text: translate.t("freeTrial.item3") },
    { text: translate.t("freeTrial.item4") },
    { text: translate.t("freeTrial.item5") },
    { text: translate.t("freeTrial.item6") },
  ];

  return (
    <Container>
      <WhiteContainer>
        <CloudImage
          alt={"Fluid Logo"}
          src={"airs/logo_fluid_attacks_2021_eqop3k"}
          styles={"absolute"}
        />
        <InternalContainer>
          <Title
            fColor={"#2e2e38"}
            fSize={"48"}
            marginBottom={"1.5"}
            maxWidth={"670"}
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
          <Link to={"https://app.fluidattacks.com/"}>
            <NewRegularRedButton>
              {translate.t("freeTrial.button")}
            </NewRegularRedButton>
          </Link>
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
