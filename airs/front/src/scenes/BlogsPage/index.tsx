import React from "react";

import { BlogsCta } from "./BlogsCta";
import { BlogsList } from "./BlogsList";
import { Header } from "./Header";

const BlogsPage: React.FC = (): JSX.Element => {
  return (
    <React.Fragment>
      <Header />
      <BlogsList />
      <BlogsCta />
    </React.Fragment>
  );
};

export { BlogsPage };
