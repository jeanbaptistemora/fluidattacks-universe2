/* eslint react/forbid-component-props: 0 */
import React from "react";

interface IProps {
  link: string;
  name: string;
}

const bodyLinkStyles: string = `
  c-blue-gray
  roboto
  f6
  fw4
  no-underline
  hv-fluid-dkred
`;

const BodyLink: React.FC<IProps> = ({ link, name }: IProps): JSX.Element => (
  <a className={bodyLinkStyles} href={link}>
    {name}
  </a>
);

export { BodyLink };
