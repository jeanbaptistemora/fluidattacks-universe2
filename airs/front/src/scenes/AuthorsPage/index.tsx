import React from "react";

import { AuthorsList } from "./AuthorsList";
import { Cta } from "./Cta";
import { Header } from "./Header";

const AuthorsPage: React.FC = (): JSX.Element => {
  return (
    <React.Fragment>
      <Header />
      <AuthorsList />
      <Cta />
    </React.Fragment>
  );
};

export { AuthorsPage };
