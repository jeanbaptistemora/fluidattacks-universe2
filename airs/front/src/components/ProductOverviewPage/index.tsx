import React from "react";

import { CardsSection } from "./CardsSection";
import { FaqSection } from "./FaqSection";
import { MainSection } from "./MainSection";
import { PlansSection } from "./PlansSection";
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
      <MainSection description={description} />
      <CardsSection />
      <PlansSection />
      <FaqSection />
      <Portrait />
    </PageArticle>
  );
};

export { ProductOverviewPage };
