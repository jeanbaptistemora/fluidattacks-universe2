import React from "react";

import { HeaderSection } from "./HeaderSection";
import { MainSection } from "./MainSection";

interface ISolutionPageProps {
  description: string;
  htmlAst: string;
  image: string;
  title: string;
}

const SolutionPage: React.FC<ISolutionPageProps> = ({
  description,
  htmlAst,
  image,
  title,
}): JSX.Element => {
  return (
    <React.Fragment>
      <HeaderSection description={description} image={image} title={title} />
      <MainSection htmlAst={htmlAst} />
    </React.Fragment>
  );
};

export { SolutionPage };
