/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type React from "react";
import styled from "styled-components";

type ExternalLinkProps = Omit<
  React.AnchorHTMLAttributes<HTMLAnchorElement>,
  "rel" | "target"
>;

const ExternalLink = styled.a.attrs<ExternalLinkProps>({
  className: "comp-ext-link f6 link",
  // https://owasp.org/www-community/attacks/Reverse_Tabnabbing
  rel: "nofollow noopener noreferrer",
  target: "_blank",
})`
  border-radius: 4px;
  color: #5c5c70;
  padding: 6px;
  text-decoration: underline;
  :hover {
    background-color: #dddde3;
    color: #121216;
  }
`;

export type { ExternalLinkProps };
export { ExternalLink };
