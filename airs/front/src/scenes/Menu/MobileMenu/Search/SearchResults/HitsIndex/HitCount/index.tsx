/* eslint @typescript-eslint/no-unnecessary-condition:0 */
import React from "react";
import { connectStateResults } from "react-instantsearch-dom";

export const HitCount = connectStateResults(
  ({ searchResults }: { searchResults: { nbHits: number } }): JSX.Element => {
    if (searchResults?.nbHits > 0) {
      return (
        <div className={"HitCount pb3"}>
          {`
          ${searchResults?.nbHits} result${
            searchResults?.nbHits === 1 ? "" : "s"
          }`}
        </div>
      );
    }

    return <div />;
  }
);
