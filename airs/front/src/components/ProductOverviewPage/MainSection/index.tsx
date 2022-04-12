/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import {
  Container,
  GifContainer,
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
        <GifContainer>
          <img
            alt={"Product Overview"}
            src={
              "https://res.cloudinary.com/fluid-attacks/image/upload/v1649707384/airs/product-overview/product-overview-video.gif"
            }
          />
        </GifContainer>
      </FullWidthContainer>
    </Container>
  );
};

export { MainSection };
