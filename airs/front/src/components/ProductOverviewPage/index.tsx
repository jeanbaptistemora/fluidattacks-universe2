/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { Banner } from "./Banner";
import { CardsSection } from "./CardsSection";
import { ClientsSection } from "./ClientsSection";
import { MainSection } from "./MainSection";
import { PlansBanner } from "./PlansBanner";
import { ProductSection } from "./ProductSection";

import { PageArticle } from "../../styles/styledComponents";

interface IProps {
  description: string;
}

const ProductOverviewPage: React.FC<IProps> = ({
  description,
}: IProps): JSX.Element => {
  return (
    <PageArticle bgColor={"#f9f9f9"}>
      <MainSection description={description} />
      <CardsSection />
      <ProductSection />
      <PlansBanner />
      <ClientsSection
        sectionColor={"#2e2e38"}
        titleColor={"#f4f4f6"}
        titleSize={"24"}
      />
      <Banner />
    </PageArticle>
  );
};

export { ProductOverviewPage };
