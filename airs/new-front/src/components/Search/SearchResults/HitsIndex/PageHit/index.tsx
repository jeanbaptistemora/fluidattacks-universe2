/* eslint react/forbid-component-props:0 */
import { faLink } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "gatsby";
import React from "react";
import { Snippet } from "react-instantsearch-dom";

export const PageHit = ({
  hit,
}: {
  hit: { pageAttributes: { slug: string }; title: string };
}): JSX.Element => (
  <Link to={`/${hit.pageAttributes.slug}`}>
    <div className={"HitDiv bg-white pv2 ph1 br3 bs-btm-h-5 t-all-3-eio"}>
      <h4 className={"dib t-all-3-eio"}>{hit.title}</h4>
      <Snippet attribute={"excerpt"} hit={hit} tagName={"mark"} />
      <FontAwesomeIcon
        className={"fr pb4 dib pr3 c-fluid-gray f4"}
        icon={faLink}
      />
    </div>
  </Link>
);
