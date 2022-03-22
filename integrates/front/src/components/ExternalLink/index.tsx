import type React from "react";
import styled from "styled-components";

type ExternalLinkProps = Omit<
  React.AnchorHTMLAttributes<HTMLAnchorElement>,
  "rel" | "target"
>;

const ExternalLink = styled.a.attrs<ExternalLinkProps>({
  className: "link",
  // https://owasp.org/www-community/attacks/Reverse_Tabnabbing
  rel: "nofollow noopener noreferrer",
  target: "_blank",
})``;

export { ExternalLink, ExternalLinkProps };
