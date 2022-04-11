/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import {
  Container,
  MainTextContainer,
  ProductParagraph,
} from "./styledComponents";

import {
  FullWidthContainer,
  NewBlackBigParagraph,
} from "../../../styles/styledComponents";
import { translate } from "../../../utils/translations/translate";
import { CloudImage } from "../../CloudImage";
import { BigRegularRedButton } from "../styledComponents";

interface IProps {
  description: string;
}

const MainSection: React.FC<IProps> = ({
  description,
}: IProps): JSX.Element => {
  return (
    <Container>
      <FullWidthContainer>
        <CloudImage
          alt={"Fluid Attacks Product"}
          src={"/airs/logo_fluid_attacks_2021_eqop3k"}
          styles={"flex center mt5"}
        />
      </FullWidthContainer>
      <MainTextContainer>
        <NewBlackBigParagraph>
          {translate.t("productOverview.title")}
        </NewBlackBigParagraph>
        <ProductParagraph isSecundary={false}>{description}</ProductParagraph>
        <Link to={"/contact-us-demo/"}>
          <BigRegularRedButton>
            {translate.t("productOverview.mainButton")}
          </BigRegularRedButton>
        </Link>
      </MainTextContainer>
      <FullWidthContainer>
        <CloudImage
          alt={"Product Overview"}
          src={"/airs/product-overview/product-overview-video"}
          styles={"flex center mb5 w-60-l w-100"}
        />
      </FullWidthContainer>
    </Container>
  );
};

export { MainSection };
