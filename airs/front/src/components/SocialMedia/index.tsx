/* eslint import/no-unresolved:0 */
/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
import {
  faFacebookF,
  faInstagram,
  faLinkedinIn,
  faTwitter,
  faYoutube,
} from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { SocialMediaLink } from "../../styles/styledComponents";

const SocialMedia: React.FC = (): JSX.Element => (
  <React.Fragment>
    <SocialMediaLink href={"https://www.instagram.com/fluidattacks/"}>
      <FontAwesomeIcon className={"f4 c-fluid-gray"} icon={faInstagram} />
    </SocialMediaLink>
    <SocialMediaLink
      href={"https://www.facebook.com/Fluid-Attacks-267692397253577/"}
    >
      <FontAwesomeIcon className={"f4 c-fluid-gray"} icon={faFacebookF} />
    </SocialMediaLink>
    <SocialMediaLink href={"https://www.linkedin.com/company/fluidattacks/"}>
      <FontAwesomeIcon className={"f4 c-fluid-gray"} icon={faLinkedinIn} />
    </SocialMediaLink>
    <SocialMediaLink href={"https://twitter.com/fluidattacks/"}>
      <FontAwesomeIcon className={"f4 c-fluid-gray"} icon={faTwitter} />
    </SocialMediaLink>
    <SocialMediaLink href={"https://www.youtube.com/c/fluidattacks/"}>
      <FontAwesomeIcon className={"f4 c-fluid-gray"} icon={faYoutube} />
    </SocialMediaLink>
  </React.Fragment>
);

export { SocialMedia };
