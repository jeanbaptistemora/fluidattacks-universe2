/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import { CardContainer, Container } from "./styledComponents";

import {
  NewRegularRedButton,
  PhantomRegularRedButton,
} from "../../../styles/styledComponents";
import { translate } from "../../../utils/translations/translate";
import { Paragraph, Title } from "../../Texts";

const Banner: React.FC = (): JSX.Element => {
  return (
    <Container>
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
        <Link to={"/free-trial/"}>
          <NewRegularRedButton className={"mh2 mv3"}>
            {translate.t("productOverview.mainButton1")}
          </NewRegularRedButton>
        </Link>
        <Link to={"/contact-us-demo/"}>
          <PhantomRegularRedButton className={"mh2"}>
            {translate.t("productOverview.mainButton2")}
          </PhantomRegularRedButton>
        </Link>
      </CardContainer>
    </Container>
  );
};

export { Banner };
