/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

interface IProps {
  link: string;
  name: string;
}

const headLinksStyles: string = `
  c-fluid-gray
  f4
  roboto
  fw3
  mt0-l
  no-underline
  hv-fluid-dkred
`;

const HeadLink: React.FC<IProps> = ({ link, name }: IProps): JSX.Element => (
  <Link className={headLinksStyles} to={link}>
    {name}
  </Link>
);

export { HeadLink };
