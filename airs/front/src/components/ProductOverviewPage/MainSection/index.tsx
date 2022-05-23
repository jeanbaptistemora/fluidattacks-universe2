/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import {
  Container,
  MainTextContainer,
  ProductParagraph,
} from "./styledComponents";

import {
  FlexCenterItemsContainer,
  FullWidthContainer,
  NewRegularRedButton,
  PhantomRegularRedButton,
  Title,
} from "../../../styles/styledComponents";
import { translate } from "../../../utils/translations/translate";
import { CloudImage } from "../../CloudImage";

interface IProps {
  description: string;
}

const MainSection: React.FC<IProps> = ({
  description,
}: IProps): JSX.Element => {
  return (
    <Container>
      <MainTextContainer>
        <Title
          fColor={"#f4f4f6"}
          fSizeL={"72px"}
          fSizeM={"64px"}
          fSizeS={"48px"}
        >
          {translate.t("productOverview.title")}
        </Title>
        <ProductParagraph>{description}</ProductParagraph>
        <FlexCenterItemsContainer className={"flex-wrap"}>
          <Link to={"/contact-us-demo/"}>
            <NewRegularRedButton className={"mh2 mv3"}>
              {translate.t("productOverview.mainButton1")}
            </NewRegularRedButton>
          </Link>
          <Link to={"/contact-us-demo/"}>
            <PhantomRegularRedButton className={"mh2"}>
              {translate.t("productOverview.mainButton2")}
            </PhantomRegularRedButton>
          </Link>
        </FlexCenterItemsContainer>
      </MainTextContainer>
      <FullWidthContainer>
        <CloudImage
          alt={"hero-product-overview"}
          src={"airs/product-overview/portrait/product-hero"}
          styles={"center flex"}
        />
      </FullWidthContainer>
    </Container>
  );
};

export { MainSection };
