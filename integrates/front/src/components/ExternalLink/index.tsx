import React from "react";

type ExternalLinkProps = Omit<
  React.AnchorHTMLAttributes<HTMLAnchorElement>,
  "rel" | "target"
>;

const ExternalLink: React.FC<ExternalLinkProps> = ({
  children,
  className,
  download,
  href,
}: ExternalLinkProps): JSX.Element => (
  <a
    className={className}
    download={download}
    href={href}
    // https://owasp.org/www-community/attacks/Reverse_Tabnabbing
    rel={"noopener noreferrer"}
    target={"_blank"}
  >
    {children}
  </a>
);

export { ExternalLink };
