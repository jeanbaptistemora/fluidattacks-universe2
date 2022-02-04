/* eslint import/no-unresolved:0 */
/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import {
  FaFacebookF,
  FaInstagram,
  FaLinkedinIn,
  FaTwitter,
  FaYoutube,
} from "react-icons/fa";

import { SocialMediaLink } from "../../styles/styledComponents";

const SocialMedia: React.FC = (): JSX.Element => (
  <React.Fragment>
    <Link
      className={"no-underline mr1"}
      to={"https://www.facebook.com/Fluid-Attacks-267692397253577/"}
    >
      <SocialMediaLink>
        <FaFacebookF className={"f3 c-fluid-gray mh1"} />
      </SocialMediaLink>
    </Link>
    <Link
      className={"no-underline mh1"}
      to={"https://www.linkedin.com/company/fluidattacks/"}
    >
      <SocialMediaLink>
        <FaLinkedinIn className={"f3 c-fluid-gray"} />
      </SocialMediaLink>
    </Link>
    <Link
      className={"no-underline mh1"}
      to={"https://twitter.com/fluidattacks/"}
    >
      <SocialMediaLink>
        <FaTwitter className={"f3 c-fluid-gray"} />
      </SocialMediaLink>
    </Link>
    <Link
      className={"no-underline mh1"}
      to={"https://www.youtube.com/c/fluidattacks/"}
    >
      <SocialMediaLink>
        <FaYoutube className={"f3 c-fluid-gray"} />
      </SocialMediaLink>
    </Link>
    <Link
      className={"no-underline mh1"}
      to={"https://www.instagram.com/fluidattacks/"}
    >
      <SocialMediaLink>
        <FaInstagram className={"f3 c-fluid-gray"} />
      </SocialMediaLink>
    </Link>
  </React.Fragment>
);

export { SocialMedia };
