/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

interface IColProps {
  lg?: number;
  md?: number;
  sm?: number;
  paddingTop?: number;
}

const getAttrs = (cols?: number): string =>
  cols === undefined
    ? "flex-grow: 1;"
    : `width: calc(${cols}00% / var(--cols));`;

/**
 * @param lg Amount of cols taken from nearest Row in large screens
 * @param md Amount of cols taken from nearest Row in medium screens
 * @param sm Amount of cols taken from nearest Row in small screens
 */
const Col = styled.div.attrs({
  className: "comp-col",
})<IColProps>`
  word-break: break-word;

  ${({ paddingTop }): string => `
  padding-top: ${paddingTop === undefined ? 0 : paddingTop}px;
`}

  @media (max-width: 768px) {
    ${({ sm }): string => getAttrs(sm)}
  }

  @media (min-width: 768px) and (max-width: 992px) {
    ${({ md }): string => getAttrs(md)}
  }

  @media (min-width: 992px) {
    ${({ lg }): string => getAttrs(lg)}
  }

  > .comp-card {
    height: 100%;
  }
`;

export { Col };
