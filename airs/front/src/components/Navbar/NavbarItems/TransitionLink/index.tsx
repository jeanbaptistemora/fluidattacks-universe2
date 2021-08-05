/* eslint react/forbid-component-props: 0 */
import AniLink from "gatsby-plugin-transition-link/AniLink";
import React from "react";

interface IProps {
  children: JSX.Element | string;
  styles: string;
  to: string;
}

const TransitionLink: React.FC<IProps> = ({
  children,
  styles,
  to,
}: IProps): JSX.Element => (
  <AniLink
    bg={"#f4f4f6"}
    className={styles}
    cover={true}
    direction={"bottom"}
    to={to}
  >
    {children}
  </AniLink>
);

export { TransitionLink };
