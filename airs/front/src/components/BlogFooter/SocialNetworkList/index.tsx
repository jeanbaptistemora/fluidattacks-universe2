/* eslint react/forbid-component-props: 0 */
import React from "react";
import { FaFacebookF, FaLinkedinIn, FaTwitter } from "react-icons/fa";
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
      <FaFacebookF className={"pa2 nb1 f4 black"} />
    </FacebookShareButton>
    <LinkedinShareButton
      className={"blog-link br3 ma1"}
      title={"Share on LinkedIn"}
      url={`https://fluidattacks.com/blog/${slug}`}
    >
      <FaLinkedinIn className={"pa2 nb1 f4 black"} />
    </LinkedinShareButton>
    <TwitterShareButton
      className={"blog-link br3 ma1"}
      title={"Share on Twitter"}
      url={`https://fluidattacks.com/blog/${slug}`}
    >
      <FaTwitter className={"pa2 nb1 f4 black"} />
    </TwitterShareButton>
  </React.Fragment>
);

export { SocialNetworkList };
