/* eslint @typescript-eslint/no-unnecessary-condition:0 */
import React from "react";
import { connectStateResults } from "react-instantsearch-dom";

export const HitCount = connectStateResults(
  ({ searchResults }: { searchResults: { nbHits: number } }): JSX.Element =>
    searchResults?.nbHits > 0 ? (
      <div className={"HitCount"}>
        {`
        ${searchResults?.nbHits} result${
          searchResults?.nbHits === 1 ? "" : "s"
        }`}
      </div>
    ) : (
      <div />
    )
);
