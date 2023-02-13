import styled from "styled-components";

import type { IGridProps, Nums1To4 } from "./types";

const column = "1fr ";

const getColumns = (defaultColumns: Nums1To4, columns?: Nums1To4): string =>
  columns === undefined
    ? `grid-template-columns: ${column.repeat(defaultColumns)};`
    : `grid-template-columns: ${column.repeat(columns)};`;

const StyledGrid = styled.div.attrs<IGridProps>({
  className: "Grid",
})<IGridProps>`
  ${({
    columns,
    columnsMd,
    columnsSm,
    gap,
    pv = "16px",
    ph = "16px",
  }): string => `
      display: grid;
      gap: ${gap};
      padding-top: ${pv};
      padding-bottom: ${pv};
      padding-left: ${ph};
      padding-right: ${ph};
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
