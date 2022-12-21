import { Link } from "gatsby";
import styled from "styled-components";

import type { ILinkProps } from "./types";

const ExternalLink = styled.a<ILinkProps>`
  ${({ decoration = "underline" }): string => `
    color: inherit;
    text-decoration: ${decoration};
  `}
`;

const InternalLink = styled(Link)<ILinkProps>`
  ${({ decoration = "none" }): string => `
    color: inherit;
    text-decoration: ${decoration};
  `}
`;

export { ExternalLink, InternalLink };
