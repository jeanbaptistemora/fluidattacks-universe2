/* eslint react/forbid-component-props:0 */
import { faLink } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "gatsby";
import { decode } from "he";
import React, { useCallback } from "react";
import { Snippet } from "react-instantsearch-dom";

export const PageHit = ({
  hit,
}: {
  hit: { description?: string; keywords?: string; slug: string; title: string };
}): JSX.Element => {
  const { slug, title } = hit;
  const fixedSlug = slug.startsWith("/pages/")
    ? slug.replace("/pages/", "/")
    : slug;
  const closeMenu = useCallback((): void => {
    document.body.setAttribute("style", "overflow-y: auto;");
  }, []);

  return (
    <Link onClick={closeMenu} to={fixedSlug}>
      <div className={"HitDiv bg-white pv2 ph1 br3 bs-btm-h-5 t-all-3-eio"}>
        <h4 className={"dib t-all-3-eio"}>{decode(title)}</h4>
        <Snippet attribute={"excerpt"} hit={hit} tagName={"mark"} />
        <FontAwesomeIcon
          className={"fr pb4 dib pr3 c-fluid-gray f4"}
          icon={faLink}
        />
      </div>
    </Link>
  );
};
