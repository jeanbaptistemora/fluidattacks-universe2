import React from "react";

import { Cta } from "./Cta";
import { Header } from "./Header";
import { TagsList } from "./TagsList";

const TagsPage: React.FC = (): JSX.Element => {
  return (
    <React.Fragment>
      <Header />
      <TagsList />
      <Cta />
    </React.Fragment>
  );
};

export { TagsPage };
