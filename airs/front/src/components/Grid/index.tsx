import React from "react";

import { StyledGrid } from "./styledComponents";
import type { IGridProps } from "./types";

const Grid: React.FC<IGridProps> = ({
  children,
  columns,
  columnsMd,
  columnsSm,
  gap,
}): JSX.Element => {
  return (
    <StyledGrid
      columns={columns}
      columnsMd={columnsMd}
      columnsSm={columnsSm}
      gap={gap}
    >
      {children}
    </StyledGrid>
  );
};

export { Grid };
