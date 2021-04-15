/* eslint react/forbid-component-props: 0 */
import React from "react";

interface IProps {
  link: string;
  name: string;
}

const headLinksStyles: string = `
  c-fluid-gray
  f4
  roboto
  fw4
  mt0-l
  no-underline
  hv-fluid-dkred
`;

const HeadLink: React.FC<IProps> = ({ link, name }: IProps): JSX.Element => (
  <a className={headLinksStyles} href={link}>
    {name}
  </a>
);

export { HeadLink };
