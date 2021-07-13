/* eslint react/forbid-component-props: 0 */
import AniLink from "gatsby-plugin-transition-link/AniLink";
import React from "react";

interface IProps {
  link: string;
  name: string;
}

const bodyLinkStyles: string = `
  hv-fluid-rd
  f5
  c-blue-gray
  fw4
  no-underline
  menu-txt-trans
  roboto
`;

const closeMenu = (): void => {
  document.body.setAttribute("style", "overflow-y: auto;");
};

const BodyLink: React.FC<IProps> = ({ link, name }: IProps): JSX.Element => (
  <AniLink
    bg={"#f4f4f6"}
    className={bodyLinkStyles}
    cover={true}
    direction={"left"}
    onClick={closeMenu}
    to={link}
  >
    {name}
  </AniLink>
);

export { BodyLink };
