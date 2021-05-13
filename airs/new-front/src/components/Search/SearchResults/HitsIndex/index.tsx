import React from "react";
import { Hits, Index } from "react-instantsearch-dom";

import { HitCount } from "./HitCount";
import { PageHit } from "./PageHit";

export const HitsInIndex = ({
  index,
}: {
  index: { name: string };
}): JSX.Element => (
  <Index indexName={index.name}>
    <HitCount />
    <Hits hitComponent={PageHit} />
  </Index>
);
