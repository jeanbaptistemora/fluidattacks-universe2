/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

interface IGapProps {
  disp?: "block" | "flex" | "inline-block" | "inline";
  mh?: number;
  mv?: number;
}

const Gap = styled.div.attrs({
  className: "comp-gap",
})<IGapProps>`
  ${({ disp = "flex", mh = 4, mv = 4 }): string => `
  align-items: center;
  display: ${disp};
  margin: ${-mv}px ${-mh}px;

  > * {
    margin: ${mv}px ${mh}px;
  }
  `}
`;

export type { IGapProps };
export { Gap };
