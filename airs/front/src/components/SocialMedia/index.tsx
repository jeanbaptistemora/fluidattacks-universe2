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
import { Link } from "gatsby";
import React from "react";

import { SocialMediaLink } from "../../styles/styledComponents";

const SocialMedia: React.FC = (): JSX.Element => (
  <React.Fragment>
    <Link
      className={"no-underline mr1"}
      to={"https://www.facebook.com/Fluid-Attacks-267692397253577/"}
    >
      <SocialMediaLink>
        <FontAwesomeIcon className={"f3 c-fluid-gray mh1"} icon={faFacebookF} />
      </SocialMediaLink>
    </Link>
    <Link
      className={"no-underline mh1"}
      to={"https://www.linkedin.com/company/fluidattacks/"}
    >
      <SocialMediaLink>
        <FontAwesomeIcon className={"f3 c-fluid-gray"} icon={faLinkedinIn} />
      </SocialMediaLink>
    </Link>
    <Link
      className={"no-underline mh1"}
      to={"https://twitter.com/fluidattacks/"}
    >
      <SocialMediaLink>
        <FontAwesomeIcon className={"f3 c-fluid-gray"} icon={faTwitter} />
      </SocialMediaLink>
    </Link>
    <Link
      className={"no-underline mh1"}
      to={"https://www.youtube.com/c/fluidattacks/"}
    >
      <SocialMediaLink>
        <FontAwesomeIcon className={"f3 c-fluid-gray"} icon={faYoutube} />
      </SocialMediaLink>
    </Link>
    <Link
      className={"no-underline mh1"}
      to={"https://www.instagram.com/fluidattacks/"}
    >
      <SocialMediaLink>
        <FontAwesomeIcon className={"f3 c-fluid-gray"} icon={faInstagram} />
      </SocialMediaLink>
    </Link>
  </React.Fragment>
);

export { SocialMedia };
