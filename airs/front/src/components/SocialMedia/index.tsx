/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint import/no-unresolved:0 */
/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
import React from "react";
import {
  FaFacebookF,
  FaInstagram,
  FaLinkedinIn,
  FaTwitter,
  FaYoutube,
} from "react-icons/fa";

import { SocialMediaLink } from "../../styles/styledComponents";
import { AirsLink } from "../AirsLink";

const SocialMedia: React.FC = (): JSX.Element => (
  <React.Fragment>
    <AirsLink href={"https://www.facebook.com/Fluid-Attacks-267692397253577/"}>
      <SocialMediaLink>
        <FaFacebookF className={"f3 c-fluid-gray mh1"} />
      </SocialMediaLink>
    </AirsLink>
    <AirsLink href={"https://www.linkedin.com/company/fluidattacks/"}>
      <SocialMediaLink>
        <FaLinkedinIn className={"f3 c-fluid-gray"} />
      </SocialMediaLink>
    </AirsLink>
    <AirsLink href={"https://twitter.com/fluidattacks/"}>
      <SocialMediaLink>
        <FaTwitter className={"f3 c-fluid-gray"} />
      </SocialMediaLink>
    </AirsLink>
    <AirsLink href={"https://www.youtube.com/c/fluidattacks/"}>
      <SocialMediaLink>
        <FaYoutube className={"f3 c-fluid-gray"} />
      </SocialMediaLink>
    </AirsLink>
    <AirsLink href={"https://www.instagram.com/fluidattacks/"}>
      <SocialMediaLink>
        <FaInstagram className={"f3 c-fluid-gray"} />
      </SocialMediaLink>
    </AirsLink>
  </React.Fragment>
);

export { SocialMedia };
