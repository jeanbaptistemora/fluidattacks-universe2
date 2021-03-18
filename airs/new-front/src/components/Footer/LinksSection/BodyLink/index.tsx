/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

interface IProps {
  link: string;
  name: string;
}

const bodyLinkStyles: string = `
  c-blue-gray
  roboto
  f5
  fw2
  no-underline
  hv-fluid-dkred
`;

const BodyLink: React.FC<IProps> = ({ link, name }: IProps): JSX.Element => (
  <Link className={bodyLinkStyles} to={link}>
    {name}
  </Link>
);

export { BodyLink };
