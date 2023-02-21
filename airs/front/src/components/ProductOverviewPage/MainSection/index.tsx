/* eslint react/jsx-no-bind:0 */
/* eslint react/forbid-component-props: 0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import { Link } from "gatsby";
import React, { useCallback } from "react";

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
} from "../../../styles/styledComponents";
import { translate } from "../../../utils/translations/translate";
import { CloudImage } from "../../CloudImage";
import { Title } from "../../Texts";

interface IProps {
  description: string;
}

const MainSection: React.FC<IProps> = ({
  description,
}: IProps): JSX.Element => {
  const { trackEvent } = useMatomo();

  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({
      action: "main-free-trial-click",
      category: "product-overview",
    });
  }, [trackEvent]);

  return (
    <Container>
      <MainTextContainer>
        <Title fColor={"#f4f4f6"} fSize={"48"}>
          {translate.t("productOverview.title")}
        </Title>
        <ProductParagraph>{description}</ProductParagraph>
        <FlexCenterItemsContainer className={"flex-wrap"}>
          <Link onClick={matomoFreeTrialEvent} to={"/free-trial/"}>
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
          src={"airs/platform/portrait/product-portrait"}
          styles={"center flex product-portrait w-100"}
        />
      </FullWidthContainer>
    </Container>
  );
};

export { MainSection };
