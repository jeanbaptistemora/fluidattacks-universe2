/* eslint import/no-unresolved:0 */
/* eslint import/no-namespace:0 */
import React from "react";
import { SocialMediaLink } from "../../styles/styledComponents";
import * as facebookLogo from "../../../static/images/social-media/social-facebook.png";
import * as instagramLogo from "../../../static/images/social-media/social-instagram.png";
import * as linkedinLogo from "../../../static/images/social-media/social-linkedin.png";
import * as twitterLogo from "../../../static/images/social-media/social-twitter.png";
import * as youtubeLogo from "../../../static/images/social-media/social-youtube.png";

const SocialMedia: React.FC = (): JSX.Element => (
  <React.Fragment>
    <SocialMediaLink href={"https://www.instagram.com/fluidattacks/"}>
      <img alt={"Instagram Logo"} src={instagramLogo} />
    </SocialMediaLink>
    <SocialMediaLink
      href={"https://www.facebook.com/Fluid-Attacks-267692397253577/"}
    >
      <img alt={"Facebook Logo"} src={facebookLogo} />
    </SocialMediaLink>
    <SocialMediaLink href={"https://www.linkedin.com/company/fluidattacks/"}>
      <img alt={"LinkedIn Logo"} src={linkedinLogo} />
    </SocialMediaLink>
    <SocialMediaLink href={"https://twitter.com/fluidattacks/"}>
      <img alt={"Twitter Logo"} src={twitterLogo} />
    </SocialMediaLink>
    <SocialMediaLink href={"https://www.youtube.com/c/fluidattacks/"}>
      <img alt={"Youtube Logo"} src={youtubeLogo} />
    </SocialMediaLink>
  </React.Fragment>
);

export { SocialMedia };
