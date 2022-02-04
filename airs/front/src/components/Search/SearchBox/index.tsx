// This exclusion is necessary due to the nature of the implementation
/* eslint import/no-default-export:0 */
/* eslint react/jsx-no-bind:0 */
/* eslint react/forbid-component-props:0 */
/* eslint @typescript-eslint/no-unsafe-return:0 */
import React from "react";
import type { ReactElement } from "react";
import { RiSearchLine } from "react-icons/ri";
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
      <RiSearchLine className={"SearchIcon c-fluid-gray f-1125 mh1"} />
    </form>
  )
);
