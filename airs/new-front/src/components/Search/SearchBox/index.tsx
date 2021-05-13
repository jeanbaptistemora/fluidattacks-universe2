// This exclusion is necessary due to the nature of the implementation
/* eslint import/no-default-export:0 */
/* eslint react/jsx-no-bind:0 */
/* eslint react/forbid-component-props:0 */
/* eslint @typescript-eslint/no-unsafe-return:0 */
import { faSearch } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type { ReactElement } from "react";
import type { SearchBoxProvided } from "react-instantsearch-core";
import { connectSearchBox } from "react-instantsearch-dom";

interface IProps extends SearchBoxProvided {
  className: string;
  onFocus: () => void;
}

export default connectSearchBox(
  ({
    refine,
    currentRefinement,
    className,
    onFocus,
  }: IProps): ReactElement<string, string> => (
    <form className={className}>
      <input
        aria-label={"Search"}
        className={"SearchInput"}
        onChange={(event): void => refine(event.target.value)}
        onFocus={onFocus}
        placeholder={"Search"}
        type={"text"}
        value={currentRefinement}
      />
      <FontAwesomeIcon
        className={"SearchIcon c-fluid-bk f-1125 nr-05"}
        icon={faSearch}
      />
    </form>
  )
);
