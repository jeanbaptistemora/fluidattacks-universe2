/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import { useTranslation } from "react-i18next";

import { ResourceCard } from "./ResourceCard";
import { Container, TitleContainer } from "./styledComponents";

import {
  FlexCenterItemsContainer,
  NewRegularRedButton,
} from "../../../styles/styledComponents";
import { Title } from "../../Texts";

const ResourcesSection: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const data = [
    {
      image: "resource-1",
      url: "https://try.fluidattacks.com/us/ebook/",
    },
    {
      image: "resource-2n",
      url: "https://try.fluidattacks.com/report/cvssf/",
    },
    {
      image: "report-2022",
      url: "https://try.fluidattacks.com/state-of-attacks-2022/",
    },
    {
      image: "resource-4",
      url: "https://try.fluidattacks.com/report/owasp-samm/",
    },
  ];

  return (
    <Container>
      <TitleContainer>
        <Title fColor={"#2e2e38"} fSize={"48"}>
          {t("resources.home.title")}
        </Title>
      </TitleContainer>
      <FlexCenterItemsContainer className={"flex-wrap mv5"}>
        {data.map((card): JSX.Element => {
          return (
            <ResourceCard image={card.image} key={card.image} url={card.url} />
          );
        })}
      </FlexCenterItemsContainer>
      <FlexCenterItemsContainer className={"flex-wrap mb5 tc"}>
        <Title fColor={"#2e2e38"} fSize={"24"}>
          {t("resources.home.phrase")}
        </Title>
        <Link to={"/subscription"}>
          <NewRegularRedButton className={"w-auto-ns w-100 ml3"}>
            {t("resources.home.buttonText")}
          </NewRegularRedButton>
        </Link>
      </FlexCenterItemsContainer>
    </Container>
  );
};

export { ResourcesSection };
