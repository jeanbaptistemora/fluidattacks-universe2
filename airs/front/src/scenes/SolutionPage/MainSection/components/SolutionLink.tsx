import React from "react";

import { AirsLink } from "../../../../components/AirsLink";
import type { IAirsLinkProps } from "../../../../components/AirsLink";

const SolutionLink: React.FC<IAirsLinkProps> = ({
  children,
  href,
}): JSX.Element => (
  <AirsLink decoration={"underline"} href={href}>
    {children}
  </AirsLink>
);

export { SolutionLink };
