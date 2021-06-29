/* eslint react/forbid-component-props: 0 */
import AniLink from "gatsby-plugin-transition-link/AniLink";
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
}: IProps): JSX.Element => (
  <li className={margin}>
    <AniLink
      bg={"#f4f4f6"}
      className={headLinksStyles}
      cover={true}
      direction={"bottom"}
      onClick={closeMenu}
      to={link}
    >
      {name}
    </AniLink>
  </li>
);

export { HeadLink };
