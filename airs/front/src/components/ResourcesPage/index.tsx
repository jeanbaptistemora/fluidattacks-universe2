/* eslint react/jsx-no-bind: 0 */
/* eslint react/forbid-component-props: 0 */
import React, { useCallback, useState } from "react";

import { ResourcesCard } from "./ResourceCard";
import { ResourcesMenuElements } from "./ResourcesMenuButtons";
import {
  CardsContainer,
  MainCardContainer,
  MenuList,
  ResourcesContainer,
} from "./styledComponents";

import {
  FlexCenterItemsContainer,
  NewRegularRedButton,
  PageArticle,
} from "../../styles/styledComponents";
import { translate } from "../../utils/translations/translate";
import { AirsLink } from "../AirsLink";
import { Paragraph, Title } from "../Texts";

interface IProps {
  bannerTitle: string;
}

const ResourcesPage: React.FC<IProps> = ({
  bannerTitle,
}: IProps): JSX.Element => {
  const data = [
    {
      buttonText: translate.t("resources.cardsText.buttons.webinarButton"),
      cardType: "webinar-card",
      description: translate.t(
        "resources.cardsText.webinars.webinar1Description"
      ),
      image: "/resources/resource-card1n",
      key: "card-1",
      language: "SPANISH",
      title: translate.t("resources.cardsText.webinars.webinar1Title"),
      urlCard: "https://www.youtube.com/watch?v=tGNbQelMrFA",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.downloadButton"),
      cardType: "whitepaper-card",
      description: translate.t(
        "resources.cardsText.whitePaper.whitePaper1Description"
      ),
      image: "/resources/resource-card17n",
      key: "card-17",
      language: "ENGLISH",
      title: translate.t("resources.cardsText.whitePaper.whitePaper1Title"),
      urlCard: "https://try.fluidattacks.tech/report/cvssf/",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.downloadButton"),
      cardType: "report-card",
      description: translate.t(
        "resources.cardsText.reports.report6Description"
      ),
      image: "/resources/resource-card16n",
      key: "card-16",
      language: "ENGLISH",
      title: translate.t("resources.cardsText.reports.report6Title"),
      urlCard: "https://try.fluidattacks.tech/state-of-attacks-2022/",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.downloadButton"),
      cardType: "successstory-card",
      description: translate.t(
        "resources.cardsText.successStory.successStory1Description"
      ),
      image: "/resources/resource-card18n",
      key: "card-18",
      language: "ENGLISH",
      title: translate.t("resources.cardsText.successStory.successStory1Title"),
      urlCard: "https://try.fluidattacks.tech/case-study/payvalida/",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.downloadButton"),
      cardType: "report-card",
      description: translate.t(
        "resources.cardsText.reports.report1Description"
      ),
      image: "/resources/resource-card12n",
      key: "card-2",
      language: "ENGLISH",
      title: translate.t("resources.cardsText.reports.report1Title"),
      urlCard: "https://try.fluidattacks.tech/report/state-of-attacks-2021/",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.downloadButton"),
      cardType: "report-card",
      description: translate.t(
        "resources.cardsText.reports.report2Description"
      ),
      image: "/resources/resource-card2n",
      key: "card-3",
      language: "ENGLISH",
      title: translate.t("resources.cardsText.reports.report2Title"),
      urlCard: "https://try.fluidattacks.tech/report2020/",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.downloadButton"),
      cardType: "report-card",
      description: translate.t(
        "resources.cardsText.reports.report3Description"
      ),
      image: "/resources/resource-card13n",
      key: "card-4",
      language: "ENGLISH",
      title: translate.t("resources.cardsText.reports.report3Title"),
      urlCard: "https://fluidattacks.docsend.com/view/qkdsfs75j37k8atz",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.downloadButton"),
      cardType: "report-card",
      description: translate.t(
        "resources.cardsText.reports.report4Description"
      ),
      image: "/resources/resource-card14n",
      key: "card-5",
      language: "ENGLISH",
      title: translate.t("resources.cardsText.reports.report4Title"),
      urlCard: "https://try.fluidattacks.tech/report/owasp-benchmark/",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.downloadButton"),
      cardType: "report-card",
      description: translate.t(
        "resources.cardsText.reports.report5Description"
      ),
      image: "/resources/resource-card15n",
      key: "card-6",
      language: "ENGLISH",
      title: translate.t("resources.cardsText.reports.report5Title"),
      urlCard: "https://try.fluidattacks.tech/report/owasp-samm/",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.webinarButton"),
      cardType: "webinar-card",
      description: translate.t(
        "resources.cardsText.webinars.webinar2Description"
      ),
      image: "/resources/resource-card1n",
      key: "card-7",
      language: "SPANISH",
      title: translate.t("resources.cardsText.webinars.webinar2Title"),
      urlCard: "https://www.youtube.com/watch?v=N6nVIOsnaOA",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.webinarButton"),
      cardType: "webinar-card",
      description: translate.t(
        "resources.cardsText.webinars.webinar3Description"
      ),
      image: "/resources/resource-card3n",
      key: "card-8",
      language: "SPANISH",
      title: translate.t("resources.cardsText.webinars.webinar3Title"),
      urlCard: "https://www.youtube.com/watch?v=zUJ_kU79j7E",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.downloadButton"),
      cardType: "ebook-card",
      description: translate.t("resources.cardsText.eBooks.ebook1Description"),
      image: "/resources/resource-card5n",
      key: "card-9",
      language: "ENGLISH",
      title: translate.t("resources.cardsText.eBooks.ebook1Title"),
      urlCard: "https://try.fluidattacks.tech/us/ebook/",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.webinarButton"),
      cardType: "webinar-card",
      description: translate.t(
        "resources.cardsText.webinars.webinar4Description"
      ),
      image: "/resources/resource-card8n",
      key: "card-10",
      language: "ENGLISH",
      title: translate.t("resources.cardsText.webinars.webinar4Title"),
      urlCard: "https://www.youtube.com/watch?v=VWwqhA2LFHg",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.webinarButton"),
      cardType: "webinar-card",
      description: translate.t(
        "resources.cardsText.webinars.webinar4Description"
      ),
      image: "/resources/resource-card8n",
      key: "card-11",
      language: "SPANISH",
      title: translate.t("resources.cardsText.webinars.webinar4Title"),
      urlCard: "https://www.youtube.com/watch?v=uGnccQg8Zfc",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.webinarButton"),
      cardType: "webinar-card",
      description: translate.t(
        "resources.cardsText.webinars.webinar5Description"
      ),
      image: "/resources/resource-card3n",
      key: "card-12",
      language: "SPANISH",
      title: translate.t("resources.cardsText.webinars.webinar5Title"),
      urlCard: "https://www.youtube.com/watch?v=4MS3Glq4dv8",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.webinarButton"),
      cardType: "webinar-card",
      description: translate.t(
        "resources.cardsText.webinars.webinar6Description"
      ),
      image: "/resources/resource-card9n",
      key: "card-13",
      language: "SPANISH",
      title: translate.t("resources.cardsText.webinars.webinar6Title"),
      urlCard: "https://www.youtube.com/watch?v=8DXafdNIZ-4",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.webinarButton"),
      cardType: "webinar-card",
      description: translate.t(
        "resources.cardsText.webinars.webinar7Description"
      ),
      image: "/resources/resource-card8n",
      key: "card-14",
      language: "ENGLISH",
      title: translate.t("resources.cardsText.webinars.webinar7Title"),
      urlCard: "https://www.youtube.com/watch?v=NoI3PWnTUak",
    },
    {
      buttonText: translate.t("resources.cardsText.buttons.webinarButton"),
      cardType: "webinar-card",
      description: translate.t(
        "resources.cardsText.webinars.webinar8Description"
      ),
      image: "/resources/resource-card11n",
      key: "card-15",
      language: "SPANISH",
      title: translate.t("resources.cardsText.webinars.webinar8Title"),
      urlCard: "https://www.youtube.com/watch?reload=9&v=-KvvMD7EJAs",
    },
  ];

  const [filteredData, setFilteredData] = useState(data);

  const filterData = useCallback(
    (type: string): void => {
      if (type === "all-card") {
        setFilteredData(data);
      } else {
        setFilteredData(
          data.filter(
            (resourcesCards): boolean => resourcesCards.cardType === type
          )
        );
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  return (
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
          <AirsLink href={"https://docs.fluidattacks.com/criteria/"}>
            <NewRegularRedButton className={"w-40-ns w-100"}>
              {translate.t("resources.elementsText.rules.rulesButton")}
            </NewRegularRedButton>
          </AirsLink>
        </MainCardContainer>
        <MenuList>
          <ResourcesMenuElements filterData={filterData} />
        </MenuList>
        <CardsContainer>
          {filteredData.map((resourceCard): JSX.Element => {
            return (
              <ResourcesCard
                buttonText={resourceCard.buttonText}
                cardType={resourceCard.cardType}
                description={resourceCard.description}
                image={resourceCard.image}
                key={resourceCard.key}
                language={resourceCard.language}
                title={resourceCard.title}
                urlCard={resourceCard.urlCard}
              />
            );
          })}
        </CardsContainer>
      </ResourcesContainer>
    </PageArticle>
  );
};

export { ResourcesPage };
