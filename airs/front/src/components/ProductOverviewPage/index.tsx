import React from "react";

import { CardsSection } from "./CardsSection";
import { PlanSection } from "./PlanSection";

import { PageArticle } from "../../styles/styledComponents";

interface IProps {
  description: string;
}

const ProductOverviewPage: React.FC<IProps> = ({
  description,
}: IProps): JSX.Element => {
  return (
    <PageArticle>
      <PlanSection description={description} />
      <CardsSection />
    </PageArticle>
  );
};

export { ProductOverviewPage };
