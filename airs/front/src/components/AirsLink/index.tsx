import React from "react";

import { ExternalLink, InternalLink } from "./styledComponents";
import type { ILinkProps } from "./types";

interface IAirsLinkProps extends ILinkProps {
  children: React.ReactNode;
  href: string;
}

const AirsLink: React.FC<IAirsLinkProps> = ({
  children,
  decoration,
  href,
}): JSX.Element => {
  const allowLinks = [
    "https://status.fluidattacks.com",
    "https://docs.fluidattacks.com",
    "https://try.fluidattacks.com",
    "https://app.fluidattacks.com",
    "https://www.instagram.com/fluidattacks",
    "https://www.facebook.com/Fluid-Attacks-267692397253577/",
    "https://twitter.com/fluidattacks",
    "https://www.youtube.com/c/fluidattacks",
    "https://www.linkedin.com/company/fluidattacks",
  ];

  if (allowLinks.some((link): boolean => href.startsWith(link))) {
    return (
      <ExternalLink
        decoration={decoration}
        href={href}
        rel={"noopener noreferrer"}
        target={"_blank"}
      >
        {children}
      </ExternalLink>
    );
  } else if (href.startsWith("https://") || href.startsWith("http://")) {
    return (
      <ExternalLink
        decoration={decoration}
        href={href}
        rel={"nofollow noopener noreferrer"}
        target={"_blank"}
      >
        {children}
      </ExternalLink>
    );
  }

  return (
    <InternalLink decoration={decoration} to={href}>
      {children}
    </InternalLink>
  );
};

export { AirsLink };
export type { IAirsLinkProps };
