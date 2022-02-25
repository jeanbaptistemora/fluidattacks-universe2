/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import { useTranslation } from "react-i18next";

import { ResourceCard } from "./ResourceCard";
import { BlackParagraph, Container, TitleContainer } from "./styledComponents";

import {
  FlexCenterItemsContainer,
  NewBlackBigParagraph,
  NewRegularRedButton,
} from "../../../styles/styledComponents";

const ResourcesSection: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const data = [
    {
      image: "resource-1",
      url: "https://landing.fluidattacks.com/us/ebook/",
    },
    {
      image: "resource-2",
      url: "https://fluidattacks.docsend.com/view/g7zbsrdi8fbnd85m",
    },
    {
      image: "resource-3",
      url: "https://try.fluidattacks.com/report/state-of-attacks-2021/",
    },
    {
      image: "resource-4",
      url: "https://fluidattacks.docsend.com/view/4k524b3gviwqubri",
    },
  ];

  return (
    <Container>
      <TitleContainer>
        <NewBlackBigParagraph>{t("resources.home.title")}</NewBlackBigParagraph>
      </TitleContainer>
      <FlexCenterItemsContainer className={"flex-wrap mv5"}>
        {data.map((card): JSX.Element => {
          return (
            <ResourceCard image={card.image} key={card.image} url={card.url} />
          );
        })}
      </FlexCenterItemsContainer>
      <FlexCenterItemsContainer className={"flex-wrap mb5 tc"}>
        <BlackParagraph>{t("resources.home.phrase")}</BlackParagraph>
        <Link to={"/subscription"}>
          <NewRegularRedButton className={"w-auto-ns w-100"}>
            {t("resources.home.buttonText")}
          </NewRegularRedButton>
        </Link>
      </FlexCenterItemsContainer>
    </Container>
  );
};

export { ResourcesSection };
