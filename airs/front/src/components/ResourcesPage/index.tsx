/* eslint react/forbid-component-props: 0 */
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { ResourcesCard } from "./ResourceCard";
import { ResourcesElement } from "./ResourcesElement";
import { ResourcesMenuElements } from "./ResourcesMenuButtons";

import {
  BannerContainer,
  BannerSubtitle,
  BannerTitle,
  BlogPageArticle,
  FullWidthContainer,
} from "../../styles/styledComponents";
import { translate } from "../../utils/translations/translate";

interface IProps {
  bannerTitle: string;
}

const MenuList: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
      list
      ph0-ns
      ph3
      ma0
      tc
      pv3
    `,
})``;

const CardsContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    roboto
    flex-ns
    flex-wrap-ns
    justify-between-m
    mw-1366
    pv4-l
    pv3
    bg-gray-221
    ml-auto
    mr-auto
    `,
})``;

const ResourcesPage: React.FC<IProps> = ({
  bannerTitle,
}: IProps): JSX.Element => (
  <BlogPageArticle>
    <BannerContainer className={"resources-bg"}>
      <FullWidthContainer>
        <BannerTitle>{bannerTitle}</BannerTitle>
        <BannerSubtitle>
          {translate.t("resources.elementsText.banner.subTitle")}
        </BannerSubtitle>
      </FullWidthContainer>
    </BannerContainer>
    <ResourcesElement
      buttonDescription={`${translate.t(
        "resources.elementsText.rules.rulesButton"
      )}`}
      description={`${translate.t(
        "resources.elementsText.rules.rulesDescription"
      )}`}
      direction={"https://docs.fluidattacks.com/criteria/"}
      image={"/resources/resource-rules_roxdew"}
      imageSide={"center"}
      textSide={"center"}
      title={`${translate.t("resources.elementsText.rules.rulesTitle")}`}
    />
    <MenuList>
      <ResourcesMenuElements />
    </MenuList>
    <CardsContainer>
      <ResourcesCard
        buttonText={`${translate.t(
          "resources.cardsText.buttons.webinarButton"
        )}`}
        cardType={"webinar-card"}
        description={`${translate.t(
          "resources.cardsText.webinars.webinar1Description"
        )}`}
        image={"/resources/resource-card1n"}
        language={"ESP"}
        title={`${translate.t("resources.cardsText.webinars.webinar1Title")}`}
        urlCard={
          "https://www.gotostage.com/channel/d38612ee120645cd93ac5ef7f65119f6/recording/287e90418c824496b67638480010f2b4/watch"
        }
      />
      <ResourcesCard
        buttonText={`${translate.t(
          "resources.cardsText.buttons.downloadButton"
        )}`}
        cardType={"report-card"}
        description={`${translate.t(
          "resources.cardsText.reports.report1Description"
        )}`}
        image={"/resources/resource-card12n"}
        language={"Webinar cover ESP"}
        title={`${translate.t("resources.cardsText.reports.report1Title")}`}
        urlCard={"https://try.fluidattacks.com/report/state-of-attacks-2021/"}
      />
      <ResourcesCard
        buttonText={`${translate.t(
          "resources.cardsText.buttons.downloadButton"
        )}`}
        cardType={"report-card"}
        description={`${translate.t(
          "resources.cardsText.reports.report2Description"
        )}`}
        image={"/resources/resource-card2n"}
        language={"Webinar cover ESP"}
        title={`${translate.t("resources.cardsText.reports.report2Title")}`}
        urlCard={"https://report2020.fluidattacks.com/"}
      />
      <ResourcesCard
        buttonText={`${translate.t(
          "resources.cardsText.buttons.downloadButton"
        )}`}
        cardType={"report-card"}
        description={`${translate.t(
          "resources.cardsText.reports.report3Description"
        )}`}
        image={"/resources/resource-card13n"}
        language={"Webinar cover ESP"}
        title={`${translate.t("resources.cardsText.reports.report3Title")}`}
        urlCard={"https://fluidattacks.docsend.com/view/qkdsfs75j37k8atz"}
      />
      <ResourcesCard
        buttonText={`${translate.t(
          "resources.cardsText.buttons.webinarButton"
        )}`}
        cardType={"webinar-card"}
        description={`${translate.t(
          "resources.cardsText.webinars.webinar2Description"
        )}`}
        image={"/resources/resource-card1n"}
        language={"ESP"}
        title={`${translate.t("resources.cardsText.webinars.webinar2Title")}`}
        urlCard={
          "https://register.gotowebinar.com/register/1684905226222105611"
        }
      />
      <ResourcesCard
        buttonText={`${translate.t(
          "resources.cardsText.buttons.webinarButton"
        )}`}
        cardType={"webinar-card"}
        description={`${translate.t(
          "resources.cardsText.webinars.webinar3Description"
        )}`}
        image={"/resources/resource-card3n"}
        language={"ESP"}
        title={`${translate.t("resources.cardsText.webinars.webinar3Title")}`}
        urlCard={
          "https://www.gotostage.com/channel/d38612ee120645cd93ac5ef7f65119f6/recording/702df3005c534f6992ad60bffc63bdee/watch"
        }
      />
      <ResourcesCard
        buttonText={`${translate.t(
          "resources.cardsText.buttons.downloadButton"
        )}`}
        cardType={"ebook-card"}
        description={`${translate.t(
          "resources.cardsText.eBooks.ebook1Description"
        )}`}
        image={"/resources/resource-card5n"}
        language={"Webinar cover ESP"}
        title={`${translate.t("resources.cardsText.eBooks.ebook1Title")}`}
        urlCard={"https://landing.fluidattacks.com/us/ebook/"}
      />
      <ResourcesCard
        buttonText={`${translate.t(
          "resources.cardsText.buttons.webinarButton"
        )}`}
        cardType={"webinar-card"}
        description={`${translate.t(
          "resources.cardsText.webinars.webinar4Description"
        )}`}
        image={"/resources/resource-card8n"}
        language={"ENG"}
        title={`${translate.t("resources.cardsText.webinars.webinar4Title")}`}
        urlCard={
          "https://register.gotowebinar.com/register/3700452970867466510"
        }
      />
      <ResourcesCard
        buttonText={`${translate.t(
          "resources.cardsText.buttons.webinarButton"
        )}`}
        cardType={"webinar-card"}
        description={`${translate.t(
          "resources.cardsText.webinars.webinar4Description"
        )}`}
        image={"/resources/resource-card8n"}
        language={"ESP"}
        title={`${translate.t("resources.cardsText.webinars.webinar4Title")}`}
        urlCard={
          "https://register.gotowebinar.com/register/8330343603644644110"
        }
      />
      <ResourcesCard
        buttonText={`${translate.t(
          "resources.cardsText.buttons.webinarButton"
        )}`}
        cardType={"webinar-card"}
        description={`${translate.t(
          "resources.cardsText.webinars.webinar5Description"
        )}`}
        image={"/resources/resource-card3n"}
        language={"ESP"}
        title={`${translate.t("resources.cardsText.webinars.webinar5Title")}`}
        urlCard={
          "https://register.gotowebinar.com/register/3618185313140820236"
        }
      />
      <ResourcesCard
        buttonText={`${translate.t(
          "resources.cardsText.buttons.webinarButton"
        )}`}
        cardType={"webinar-card"}
        description={`${translate.t(
          "resources.cardsText.webinars.webinar6Description"
        )}`}
        image={"/resources/resource-card9n"}
        language={"ESP"}
        title={`${translate.t("resources.cardsText.webinars.webinar6Title")}`}
        urlCard={
          "https://register.gotowebinar.com/register/6501685343309054732"
        }
      />
      <ResourcesCard
        buttonText={`${translate.t(
          "resources.cardsText.buttons.webinarButton"
        )}`}
        cardType={"webinar-card"}
        description={`${translate.t(
          "resources.cardsText.webinars.webinar7Description"
        )}`}
        image={"/resources/resource-card8n"}
        language={"ENG"}
        title={`${translate.t("resources.cardsText.webinars.webinar7Title")}`}
        urlCard={
          "https://register.gotowebinar.com/register/1179192545930222092"
        }
      />
      <ResourcesCard
        buttonText={`${translate.t(
          "resources.cardsText.buttons.webinarButton"
        )}`}
        cardType={"webinar-card"}
        description={`${translate.t(
          "resources.cardsText.webinars.webinar8Description"
        )}`}
        image={"/resources/resource-card11n"}
        language={"ESP"}
        title={`${translate.t("resources.cardsText.webinars.webinar8Title")}`}
        urlCard={"https://www.youtube.com/watch?reload=9&v=-KvvMD7EJAs"}
      />
    </CardsContainer>
  </BlogPageArticle>
);

export { ResourcesPage };
