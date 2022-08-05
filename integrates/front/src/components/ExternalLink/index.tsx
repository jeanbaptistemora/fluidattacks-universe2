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
  padding: 9px 6px;
  text-decoration: underline;
  :hover {
    background-color: #dddde3;
    color: #121216;
  }
`;

export type { ExternalLinkProps };
export { ExternalLink };
