/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    db
    tc
    pv5
    center
    ph-body
  `,
})<{ bgColor: string }>`
  background-color: ${({ bgColor }): string => bgColor};
`;

export { Container };
