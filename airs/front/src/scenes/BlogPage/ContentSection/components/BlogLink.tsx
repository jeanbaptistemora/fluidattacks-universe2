import React from "react";

import { AirsLink } from "../../../../components/AirsLink";
import type { IAirsLinkProps } from "../../../../components/AirsLink";

const BlogLink: React.FC<IAirsLinkProps> = ({
  children,
  href,
}): JSX.Element => (
  <AirsLink decoration={"underline"} hoverColor={"#bf0b1a"} href={href}>
    {children}
  </AirsLink>
);

export { BlogLink };
