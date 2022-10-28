/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

interface IProps {
  link: string;
  name: string;
}

const headLinksStyles: string = `
  c-fluid-gray
  f4
  poppins
  fw4
  mt0-l
  no-underline
  hv-fluid-dkred
`;

const HeadLink: React.FC<IProps> = ({ link, name }: IProps): JSX.Element =>
  link.startsWith("https://") || link.startsWith("http://") ? (
    <a
      className={headLinksStyles}
      href={link}
      rel={"nofollow noopener noreferrer"}
      target={"_blank"}
    >
      {name}
    </a>
  ) : (
    <Link className={headLinksStyles} to={link}>
      {name}
    </Link>
  );

export { HeadLink };
