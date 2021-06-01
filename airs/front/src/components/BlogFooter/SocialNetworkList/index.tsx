/* eslint react/forbid-component-props: 0 */
import {
  faFacebookF,
  faLinkedinIn,
  faTwitter,
} from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import {
  FacebookShareButton,
  LinkedinShareButton,
  TwitterShareButton,
} from "react-share";

interface IProps {
  slug: string;
}

const SocialNetworkList: React.FC<IProps> = ({ slug }: IProps): JSX.Element => (
  <React.Fragment>
    <FacebookShareButton
      className={"blog-link br3 ma1"}
      title={"Share on Facebook"}
      url={`https://fluidattacks.com/blog/${slug}`}
    >
      <FontAwesomeIcon className={"pa2 nb1 f4 black"} icon={faFacebookF} />
    </FacebookShareButton>
    <LinkedinShareButton
      className={"blog-link br3 ma1"}
      title={"Share on LinkedIn"}
      url={`https://fluidattacks.com/blog/${slug}`}
    >
      <FontAwesomeIcon className={"pa2 nb1 f4 black"} icon={faLinkedinIn} />
    </LinkedinShareButton>
    <TwitterShareButton
      className={"blog-link br3 ma1"}
      title={"Share on Twitter"}
      url={`https://fluidattacks.com/blog/${slug}`}
    >
      <FontAwesomeIcon className={"pa2 nb1 f4 black"} icon={faTwitter} />
    </TwitterShareButton>
  </React.Fragment>
);

export { SocialNetworkList };
