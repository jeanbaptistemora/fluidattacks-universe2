/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

interface IProps {
  link: string;
  name: string;
}

const MenuLinkStyles: string = `
  hv-fluid-rd
  db
  f4
  c-fluid-bk
  mv2
  fw4
  no-underline
  menu-txt-trans
  roboto
`;

const closeMenu = (): void => {
  document.body.setAttribute("style", "overflow-y: auto;");
};

const MenuLink: React.FC<IProps> = ({ link, name }: IProps): JSX.Element => (
  <Link className={MenuLinkStyles} onClick={closeMenu} to={link}>
    {name}
  </Link>
);

export { MenuLink };
