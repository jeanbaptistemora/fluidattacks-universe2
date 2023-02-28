import { join } from "path-browserify";
import React from "react";

import {
  Breadcrumb,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbListItem,
  BreadcrumbSeparator,
} from "./StyledComponents";

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
    <Breadcrumb>
      <BreadcrumbList>
        {currentPath.map((page, index): JSX.Element => {
          // eslint-disable-next-line fp/no-mutation
          linkPath = join(linkPath, page);

          const currentPage = page === "/" ? "Home" : page;

          return (
            <BreadcrumbListItem key={currentPage}>
              {index === lastPage ? (
                <BreadcrumbLink to={linkPath}>
                  {capitalizeDashedString(page)}
                </BreadcrumbLink>
              ) : (
                <div>
                  <BreadcrumbLink to={linkPath}>
                    {capitalizeDashedString(currentPage)}
                  </BreadcrumbLink>
                  <BreadcrumbSeparator>{"/"}</BreadcrumbSeparator>
                </div>
              )}
            </BreadcrumbListItem>
          );
        })}
      </BreadcrumbList>
    </Breadcrumb>
  );
};

export { Breadcrumbs };
