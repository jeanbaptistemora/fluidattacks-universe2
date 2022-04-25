/* eslint react/forbid-component-props: 0 */
/* eslint fp/no-let: 0 */
/* eslint fp/no-mutation: 0 */
import { Link } from "gatsby";
import React from "react";

import {
  CenteredContainer,
  ContentContainer,
  OneShotBlackParagraph,
  SubmenuListItem,
} from "./styledComponents";

import {
  BannerContainer,
  BannerSubtitle,
  BigPageContainer,
  BlackH2,
  FlexCenterItemsContainer,
  FullWidthContainer,
  LittleBannerTitle,
  LittleBlackParagraph,
  PageArticle,
  RegularRedButton,
} from "../../styles/styledComponents";
import { translate } from "../../utils/translations/translate";

interface IProps {
  banner: string;
  content: string;
  definition: string;
  image: string;
  isContinuous: string;
  subtitle: string;
  title: string;
}

interface IItemsProps {
  continuous: string;
  oneShot: string;
}

const ServicePage: React.FC<IProps> = ({
  banner,
  content,
  definition,
  image,
  isContinuous,
  subtitle,
  title,
}: IProps): JSX.Element => {
  const subMenuClasses: IItemsProps = {
    continuous: "",
    oneShot: "",
  };

  const linksClasses: IItemsProps = {
    continuous: "c-fluid-bk",
    oneShot: "c-fluid-bk",
  };
  let oneShotParagraph: string = "";

  if (isContinuous === "yes") {
    subMenuClasses.continuous = "bb bc-hovered-red bw2";
    linksClasses.oneShot = "c-fluid-gray hv-fluid-black";
  } else {
    subMenuClasses.oneShot = "bb bc-hovered-red bw2";
    linksClasses.continuous = "c-fluid-gray hv-fluid-black";
    oneShotParagraph = translate.t("service.oneShotParagraph");
  }

  return (
    <PageArticle bgColor={"#f9f9f9"}>
      <BannerContainer className={banner}>
        <FullWidthContainer>
          <LittleBannerTitle>{title}</LittleBannerTitle>
          <BannerSubtitle>{subtitle}</BannerSubtitle>
        </FullWidthContainer>
      </BannerContainer>
      <FlexCenterItemsContainer className={"tc pt3 nowrap overflow-x-auto"}>
        <ul className={"pl0"}>
          <SubmenuListItem className={subMenuClasses.continuous}>
            <Link
              className={`${linksClasses.continuous} f4 roboto fw7 no-underline`}
              to={"/services/continuous-hacking/"}
            >
              {"Continuous Hacking"}
            </Link>
          </SubmenuListItem>
          <SubmenuListItem className={subMenuClasses.oneShot}>
            <Link
              className={`${linksClasses.oneShot} f4 roboto fw7 no-underline`}
              to={"/services/one-shot-hacking/"}
            >
              {"One-Shot Hacking"}
            </Link>
          </SubmenuListItem>
        </ul>
      </FlexCenterItemsContainer>

      <ContentContainer>
        <FullWidthContainer className={"pv4"}>
          <FlexCenterItemsContainer className={"flex-wrap center"}>
            <div>
              <div className={"tl"}>
                <LittleBlackParagraph>{definition}</LittleBlackParagraph>
              </div>

              <div className={"center tc"}>
                <Link to={"/contact-us/"}>
                  <RegularRedButton>{"Make an inquiry"}</RegularRedButton>
                </Link>
              </div>
            </div>
          </FlexCenterItemsContainer>
        </FullWidthContainer>
        <CenteredContainer className={"tc mv4"}>
          <img alt={title} className={"tc h5"} src={image} />
        </CenteredContainer>
      </ContentContainer>
      <BigPageContainer>
        <FullWidthContainer>
          <BlackH2>{"Key Features"}</BlackH2>
          <FlexCenterItemsContainer
            className={"internal solution-benefits services-features flex-wrap"}
            dangerouslySetInnerHTML={{
              __html: content,
            }}
          />
        </FullWidthContainer>
      </BigPageContainer>
      <ContentContainer>
        <OneShotBlackParagraph>{oneShotParagraph}</OneShotBlackParagraph>
      </ContentContainer>
    </PageArticle>
  );
};

export { ServicePage };
