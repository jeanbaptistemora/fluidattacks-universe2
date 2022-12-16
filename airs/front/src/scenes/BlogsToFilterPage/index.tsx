import React from "react";

import { BlogsCta } from "./BlogsCta";
import { BlogsList } from "./BlogsList";
import { Header } from "./Header";
import type { IBlogsToFilterPageProps } from "./types";

import { capitalizeDashedString } from "../../utils/utilities";

const BlogsToFilterPage: React.FC<IBlogsToFilterPageProps> = ({
  description = "",
  filterBy,
  title = "",
  value,
}): JSX.Element => {
  return (
    <React.Fragment>
      <Header
        description={description}
        title={title ? title : capitalizeDashedString(value)}
      />
      <BlogsList filterBy={filterBy} value={value} />
      <BlogsCta />
    </React.Fragment>
  );
};

export { BlogsToFilterPage };
