import { Link } from "gatsby";
import { join } from "path-browserify";
import React from "react";

import { capitalizeDashedString } from "../../utils/utilities";

interface IProps {
  currentPath: string[];
}

const Breadcrumbs: React.FC<IProps> = ({
  currentPath,
}: IProps): JSX.Element => {
  // eslint-disable-next-line fp/no-let
  let linkPath = "";

  const lastPage = currentPath.length > 0 ? currentPath.length - 1 : 0;

  return (
    <nav className={"breadcrumb"}>
      <ol className={"breadcrumb-list"}>
        {currentPath.map((page, index): JSX.Element => {
          // eslint-disable-next-line fp/no-mutation
          linkPath = join(linkPath, page);

          const currentPage = page === "/" ? "Home" : page;

          return (
            <li className={"breadcrumb-list-item"} key={currentPage}>
              {index === lastPage ? (
                <div className={"breadcrumb-link"}>
                  {capitalizeDashedString(page)}
                </div>
              ) : (
                <div>
                  <Link to={linkPath}>
                    {capitalizeDashedString(currentPage)}
                  </Link>
                  <div className={"breadcrumb-separator"}>{"/"}</div>
                </div>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
};

export { Breadcrumbs };
