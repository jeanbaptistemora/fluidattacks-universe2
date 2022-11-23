import { Link } from "gatsby";
import styled from "styled-components";

import type { ILinkProps } from "./types";

const InternalLink = styled(Link)<ILinkProps>`
  ${({ decoration = "none" }): string => `
    text-decoration: ${decoration};
  `}
`;

export { InternalLink };
