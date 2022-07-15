/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { ResourcesCard } from "./ResourceCard";
import { ResourcesMenuElements } from "./ResourcesMenuButtons";
import { MainCardContainer, ResourcesContainer } from "./styledComponents";

import {
  FlexCenterItemsContainer,
  NewRegularRedButton,
  PageArticle,
} from "../../styles/styledComponents";
import { translate } from "../../utils/translations/translate";
import { Paragraph, Title } from "../Texts";

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
    justify-around
    mw-1366
    ph-body
    pv4-l
    pv3
    bg-graylight
    center
    `,
})``;

const ResourcesPage: React.FC<IProps> = ({
  bannerTitle,
}: IProps): JSX.Element => (
  <PageArticle bgColor={"#dddde3"}>
    <ResourcesContainer>
      <FlexCenterItemsContainer>
        <Title fColor={"#2e2e38"} fSize={"48"} marginTop={"4"}>
          {bannerTitle}
        </Title>
      </FlexCenterItemsContainer>
      <FlexCenterItemsContainer>
        <Paragraph fColor={"#5c5c70"} fSize={"16"} marginTop={"1"}>
          {translate.t("resources.elementsText.banner.subTitle")}
        </Paragraph>
      </FlexCenterItemsContainer>
      <MainCardContainer>
        <Title fColor={"#5c5c70"} fSize={"16"}>
          {translate.t("resources.elementsText.rules.rulesDescription1")}
        </Title>
        <Title fColor={"#2e2e38"} fSize={"32"} marginTop={"1"}>
          {translate.t("resources.elementsText.rules.rulesTitle")}
        </Title>
        <Paragraph
          fColor={"#787891"}
          fSize={"24"}
          marginBottom={"1"}
          marginTop={"1"}
        >
          {translate.t("resources.elementsText.rules.rulesDescription2")}
        </Paragraph>
        <Link to={"https://docs.fluidattacks.com/criteria/"}>
          <NewRegularRedButton className={"w-40-ns w-100"}>
            {translate.t("resources.elementsText.rules.rulesButton")}
          </NewRegularRedButton>
        </Link>
      </MainCardContainer>
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
          language={"SPANISH"}
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
          language={"ENGLISH"}
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
          language={"ENGLISH"}
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
          language={"ENGLISH"}
          title={`${translate.t("resources.cardsText.reports.report3Title")}`}
          urlCard={"https://fluidattacks.docsend.com/view/qkdsfs75j37k8atz"}
        />
        <ResourcesCard
          buttonText={`${translate.t(
            "resources.cardsText.buttons.downloadButton"
          )}`}
          cardType={"report-card"}
          description={`${translate.t(
            "resources.cardsText.reports.report4Description"
          )}`}
          image={"/resources/resource-card14n"}
          language={"ENGLISH"}
          title={`${translate.t("resources.cardsText.reports.report4Title")}`}
          urlCard={"https://fluidattacks.docsend.com/view/kp8uj28i8d6us5u5"}
        />
        <ResourcesCard
          buttonText={`${translate.t(
            "resources.cardsText.buttons.downloadButton"
          )}`}
          cardType={"report-card"}
          description={`${translate.t(
            "resources.cardsText.reports.report5Description"
          )}`}
          image={"/resources/resource-card15n"}
          language={"ENGLISH"}
          title={`${translate.t("resources.cardsText.reports.report5Title")}`}
          urlCard={"https://fluidattacks.docsend.com/view/4k524b3gviwqubri"}
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
          language={"SPANISH"}
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
          language={"SPANISH"}
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
          language={"ENGLISH"}
          title={`${translate.t("resources.cardsText.eBooks.ebook1Title")}`}
          urlCard={"https://try.fluidattacks.com/us/ebook/"}
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
          language={"ENGLISH"}
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
          language={"SPANISH"}
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
          language={"SPANISH"}
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
          language={"SPANISH"}
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
          language={"ENGLISH"}
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
          language={"SPANISH"}
          title={`${translate.t("resources.cardsText.webinars.webinar8Title")}`}
          urlCard={"https://www.youtube.com/watch?reload=9&v=-KvvMD7EJAs"}
        />
      </CardsContainer>
    </ResourcesContainer>
  </PageArticle>
);

export { ResourcesPage };
