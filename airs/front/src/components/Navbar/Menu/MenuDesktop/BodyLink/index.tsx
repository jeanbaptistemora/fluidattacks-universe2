/* eslint react/forbid-component-props: 0 */
import AniLink from "gatsby-plugin-transition-link/AniLink";
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
    <AniLink
      bg={"#f4f4f6"}
      className={bodyLinkStyles}
      cover={true}
      direction={"bottom"}
      onClick={closeMenu}
      to={link}
    >
      {name}
    </AniLink>
  </li>
);

export { BodyLink };
