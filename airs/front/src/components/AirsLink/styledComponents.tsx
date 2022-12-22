import { Link } from "gatsby";
import styled from "styled-components";

import type { ILinkProps } from "./types";

const ExternalLink = styled.a<ILinkProps>`
  ${({ decoration = "underline", hoverColor = "" }): string => `
    color: inherit;
    text-decoration: ${decoration};
    text-decoration-color: inherit;

    :hover {
      color: ${hoverColor ? `${hoverColor}` : "inherit"};
      text-decoration-color: ${hoverColor ? `${hoverColor}` : "inherit"};

      p {
        color: ${hoverColor ? `${hoverColor}` : "inherit"};
      }
    }
  `}
`;

const InternalLink = styled(Link)<ILinkProps>`
  ${({ decoration = "none", hoverColor = "" }): string => `
    color: inherit;
    text-decoration: ${decoration};
    text-decoration-color: inherit;

    :hover {
      color: ${hoverColor ? `${hoverColor}` : "inherit"};
      text-decoration-color: ${hoverColor ? `${hoverColor}` : "inherit"};

      p {
        color: ${hoverColor ? `${hoverColor}` : "inherit"};
      }
    }
  `}
`;

export { ExternalLink, InternalLink };
