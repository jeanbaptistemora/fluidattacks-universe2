import styled from "styled-components";

import type { IGridProps } from "./types";

const getColumns = (defaultColumns: string, columns?: string): string =>
  columns === undefined
    ? `grid-template-columns: ${defaultColumns};`
    : `grid-template-columns: ${columns};`;

const StyledGrid = styled.div<IGridProps>`
  ${({ columns, columnsMd, columnsSm, gap }): string => `
      display: grid;
      gap: ${gap};
      @media screen and (min-width: 60em) {
        ${getColumns(columns)}
      }

      @media screen and (min-width: 30em) and (max-width: 60em) {
        ${getColumns(columns, columnsMd)}
      }

      @media screen and (max-width: 30em) {
        ${getColumns(columnsMd === undefined ? columns : columnsMd, columnsSm)}
      }
    `}
`;

export { StyledGrid };
