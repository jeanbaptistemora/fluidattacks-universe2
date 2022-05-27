import React from "react";

import { CardsSection } from "./CardsSection";
import { MainSection } from "./MainSection";
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
    </PageArticle>
  );
};

export { ProductOverviewPage };
