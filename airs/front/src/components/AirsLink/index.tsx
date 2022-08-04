/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

interface IProps {
  children: JSX.Element;
  href: string;
}

const AirsLink: React.FC<IProps> = ({ children, href }: IProps): JSX.Element =>
  href.startsWith("https://") || href.startsWith("http://") ? (
    <a href={href} rel={"nofollow noopener noreferrer"} target={"_blank"}>
      {children}
    </a>
  ) : (
    <Link to={href}>{children}</Link>
  );

export { AirsLink };
