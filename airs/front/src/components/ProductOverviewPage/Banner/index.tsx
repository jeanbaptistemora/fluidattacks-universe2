import { Link } from "gatsby";
import React from "react";

import { CardContainer, Container } from "./styledComponents";

import { NewRegularRedButton } from "../../../styles/styledComponents";
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
        <Link to={"/contact-us"}>
          <NewRegularRedButton>{"Contact sales"}</NewRegularRedButton>
        </Link>
      </CardContainer>
    </Container>
  );
};

export { Banner };
