/* eslint react/forbid-component-props: 0 */
import AniLink from "gatsby-plugin-transition-link/AniLink";
import React from "react";

interface IProps {
  link: string;
  name: string;
}

const MenuLinkStyles: string = `
  hv-fluid-rd
  db
  f4
  c-black46
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
  <AniLink
    bg={"#f4f4f6"}
    className={MenuLinkStyles}
    cover={true}
    direction={"left"}
    onClick={closeMenu}
    to={link}
  >
    {name}
  </AniLink>
);

export { MenuLink };
