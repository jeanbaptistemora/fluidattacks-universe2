/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/jsx-no-bind:0 */
/* eslint react/forbid-component-props:0 */
/* eslint @typescript-eslint/no-explicit-any:0 */
/* eslint @typescript-eslint/strict-boolean-expressions:0 */
/* eslint @typescript-eslint/no-unnecessary-condition:0 */
import algoliasearch from "algoliasearch/lite";
import type { SearchClient } from "algoliasearch/lite";
import React, { createRef, useCallback, useMemo, useState } from "react";
import type { RefObject, SetStateAction } from "react";
import { InstantSearch } from "react-instantsearch-dom";
import { ThemeProvider } from "styled-components";

import {
  StyledSearchBox,
  StyledSearchResult,
  StyledSearchRoot,
} from "./StyledComponents";
import { useClickOutside } from "./useClickOutside";

interface IProps {
  indices: { name: string; title: string }[];
}

interface IQueryProps {
  query: SetStateAction<undefined>;
}

const theme = {
  background: "white",
  faded: "#888",
  foreground: "#050505",
};

export const Search: React.FC<IProps> = ({ indices }: IProps): JSX.Element => {
  const rootRef = createRef();
  const [queryValue, setQueryValue] = useState();
  const [hasFocus, setHasFocus] = useState(false);
  const searchClient = useMemo(
    (): SearchClient =>
      algoliasearch(
        process.env.GATSBY_ALGOLIA_APP_ID as string,
        process.env.GATSBY_ALGOLIA_SEARCH_KEY as string
      ),
    []
  );

  useClickOutside(rootRef as RefObject<HTMLDivElement>, (): void =>
    setHasFocus(false)
  );

  const handleSearchState = useCallback(({ query }: IQueryProps): void => {
    setQueryValue(query);
  }, []);

  const handleOnFocus = useCallback((): void => {
    setHasFocus(true);
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <StyledSearchRoot ref={rootRef as RefObject<HTMLDivElement>}>
        <InstantSearch
          indexName={indices[0].name}
          onSearchStateChange={handleSearchState}
          searchClient={searchClient}
        >
          <StyledSearchBox className={""} onFocus={handleOnFocus} />
          <StyledSearchResult
            className={"scroll-touch bs-btm-h-10 bn"}
            indices={indices}
            show={
              (queryValue &&
                (queryValue as unknown as string).length > 0 &&
                hasFocus) as unknown as boolean
            }
          />
        </InstantSearch>
      </StyledSearchRoot>
    </ThemeProvider>
  );
};
