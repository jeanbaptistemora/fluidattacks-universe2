/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

interface IProps {
  link: string;
  name: string;
}

const bodyLinkStyles: string = `
  c-black-gray
  hv-fluid-rd
  no-underline
  nowrap
  fw1
`;

const closeMenu = (): void => {
  document.body.setAttribute("style", "overflow-y: auto;");
};

const BodyLink: React.FC<IProps> = ({ link, name }: IProps): JSX.Element => (
  <li className={"mv3"}>
    <Link className={bodyLinkStyles} onClick={closeMenu} to={link}>
      {name}
    </Link>
  </li>
);

export { BodyLink };
