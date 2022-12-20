import React from "react";

import { CategoriesList } from "./CategoriesList";
import { Cta } from "./Cta";
import { Header } from "./Header";

const CategoriesPage: React.FC = (): JSX.Element => {
  return (
    <React.Fragment>
      <Header />
      <CategoriesList />
      <Cta />
    </React.Fragment>
  );
};

export { CategoriesPage };
