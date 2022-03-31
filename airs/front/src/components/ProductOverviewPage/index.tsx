import React from "react";

import { CardsSection } from "./CardsSection";
import { FaqSection } from "./FaqSection";
import { PlanSection } from "./PlanSection";
import { Portrait } from "./Portrait";

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
      <FaqSection />
      <Portrait />
    </PageArticle>
  );
};

export { ProductOverviewPage };
