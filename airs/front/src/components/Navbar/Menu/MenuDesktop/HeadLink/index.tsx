/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

interface IProps {
  link: string;
  name: string;
  margin: string;
}

const headLinksStyles: string = `
  c-fluid-bk
  f3
  hv-fluid-rd
  roboto
  no-underline
  nowrap
`;

const closeMenu = (): void => {
  document.body.setAttribute("style", "overflow-y: auto;");
};

const HeadLink: React.FC<IProps> = ({
  link,
  name,
  margin,
}: IProps): JSX.Element =>
  link.startsWith("https://") || link.startsWith("http://") ? (
    <li className={margin}>
      <a
        className={headLinksStyles}
        href={link}
        rel={"nofollow noopener noreferrer"}
        target={"_blank"}
      >
        {name}
      </a>
    </li>
  ) : (
    <li className={margin}>
      <Link className={headLinksStyles} onClick={closeMenu} to={link}>
        {name}
      </Link>
    </li>
  );

export { HeadLink };
