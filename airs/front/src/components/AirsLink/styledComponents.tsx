/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { Link } from "gatsby";
import styled from "styled-components";

import type { ILinkProps } from "./types";

const InternalLink = styled(Link)<ILinkProps>`
  ${({ decoration = "none" }): string => `
    text-decoration: ${decoration};
  `}
`;

export { InternalLink };
