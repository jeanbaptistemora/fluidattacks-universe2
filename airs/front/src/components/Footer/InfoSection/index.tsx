/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import {
  CopyrightContainer,
  CopyrightParagraph,
  FooterInfoLink,
  FooterInfoLinksContainer,
  GrayDash,
} from "../../../styles/styledComponents";

const InfoSection: React.FC = (): JSX.Element => (
  <React.Fragment>
    <CopyrightContainer>
      <CopyrightParagraph>
        {[
          `Copyright © ${new Date().getFullYear()} Fluid Attacks.`,
          "We hack your software.",
          "All rights reserved.",
        ].join(" ")}
      </CopyrightParagraph>
    </CopyrightContainer>
    <FooterInfoLinksContainer>
      <FooterInfoLink
        href={"https://status.fluidattacks.com/"}
        rel={"nofollow noopener noreferrer"}
        target={"_blank"}
      >
        {"Service Status"}
      </FooterInfoLink>
      <GrayDash>{" - "}</GrayDash>
      <Link
        className={"c-black-gray f6 fw2 mt2 roboto no-underline hv-fluid-dkred"}
        to={"/terms-use/"}
      >
        {"Terms of Use"}
      </Link>
      <GrayDash>{" - "}</GrayDash>
      <Link
        className={"c-black-gray f6 fw2 mt2 roboto no-underline hv-fluid-dkred"}
        to={"/privacy/"}
      >
        {"Privacy Policy"}
      </Link>
      <GrayDash>{" - "}</GrayDash>
      <Link
        className={"c-black-gray f6 fw2 mt2 roboto no-underline hv-fluid-dkred"}
        to={"/cookie"}
      >
        {"Cookie Policy"}
      </Link>
    </FooterInfoLinksContainer>
  </React.Fragment>
);

export { InfoSection };
