import styled from "styled-components";

import type { ExternalLinkProps } from "./types";

const ExternalLinkStandalone = styled.a.attrs<ExternalLinkProps>({
  className: "comp-ext-link-Standalone f6 link dib",
  // https://owasp.org/www-community/attacks/Reverse_Tabnabbing
  rel: "nofollow noopener noreferrer",
  target: "_blank",
})`
  border-radius: 4px;
  color: inherit;
  font-weight: 800;
  padding: 6px;
  text-decoration: none;
  background-color: transparent;
  transition: background-color 0.1s;
  :hover {
    color: #5c5c70;
    text-decoration: none;
  }
`;
export { ExternalLinkStandalone };
