import React from "react";

import { StyledGrid } from "./styledComponents";
import type { IGridProps } from "./types";

const Grid: React.FC<IGridProps> = ({
  children,
  columns,
  columnsMd,
  columnsSm,
  gap,
  pv,
  ph,
}): JSX.Element => {
  return (
    <StyledGrid
      columns={columns}
      columnsMd={columnsMd}
      columnsSm={columnsSm}
      gap={gap}
      ph={ph}
      pv={pv}
    >
      {children}
    </StyledGrid>
  );
};

export { Grid };
