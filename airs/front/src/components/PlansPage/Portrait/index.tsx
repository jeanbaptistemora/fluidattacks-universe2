import { Link } from "gatsby";
import React from "react";

import {
  CardContainer,
  Container,
  PortraitContainer,
} from "./styledComponents";

import { NewRegularRedButton } from "../../../styles/styledComponents";
import { translate } from "../../../utils/translations/translate";
import { CloudImage } from "../../CloudImage";
import { Paragraph, Title } from "../../Texts";

const Portrait: React.FC = (): JSX.Element => {
  return (
    <Container>
      <PortraitContainer>
        <CloudImage alt={"plans-portrait"} src={"/airs/plans/portrait"} />
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
      </PortraitContainer>
    </Container>
  );
};

export { Portrait };
