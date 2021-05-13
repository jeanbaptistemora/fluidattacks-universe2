import React from "react";
import { PoweredBy } from "react-instantsearch-dom";

import { HitsInIndex } from "./HitsIndex";

interface IProps {
  indices: {
    name: string;
    title: string;
  }[];
  className: string;
}

export const SearchResult = ({ indices, className }: IProps): JSX.Element => (
  <div className={className}>
    {indices.map(
      (index: { name: string }): JSX.Element => (
        <HitsInIndex index={index} key={index.name} />
      )
    )}
    <PoweredBy />
  </div>
);
