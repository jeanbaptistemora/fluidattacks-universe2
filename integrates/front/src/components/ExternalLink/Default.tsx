/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

import type { ExternalLinkProps } from "./types";

const ExternalLink = styled.a.attrs<ExternalLinkProps>({
  className: "comp-ext-link f6 link dib",
  // https://owasp.org/www-community/attacks/Reverse_Tabnabbing
  rel: "nofollow noopener noreferrer",
  target: "_blank",
})`
  border-radius: 4px;
  color: inherit;
  padding: 6px;
  text-decoration: underline;
  background-color: transparent;
  transition: background-color 0.1s;
  :hover {
    color: #5c5c70;
    text-decoration: underline;
  }
`;

export { ExternalLink };
