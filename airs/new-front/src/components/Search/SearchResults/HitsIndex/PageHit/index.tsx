import { Link } from "gatsby";
import React from "react";
import { Highlight, Snippet } from "react-instantsearch-dom";

export const PageHit = ({ hit }: { hit: { slug: string } }): JSX.Element => (
  <div>
    <Link to={hit.slug}>
      <h4>
        <Highlight attribute={"title"} hit={hit} tagName={"mark"} />
      </h4>
    </Link>
    <Snippet attribute={"excerpt"} hit={hit} tagName={"mark"} />
  </div>
);
