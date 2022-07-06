/* eslint react/forbid-component-props: 0 */
import React from "react";
import {
  FaEllipsisH,
  FaFacebookF,
  FaLinkedinIn,
  FaTwitter,
  FaWhatsapp,
} from "react-icons/fa";
import { RWebShare } from "react-web-share";

interface IProps {
  slug: string;
}

const SocialNetworkList: React.FC<IProps> = ({ slug }: IProps): JSX.Element => (
  <RWebShare
    data={{
      title: "Share this post",
      url: `https://fluidattacks.com/blog/${slug}`,
    }}
  >
    <button className={"blog-link br3 ma1 pointer bg-transparent"}>
      <FaFacebookF className={"pa2 nb1 f4 black"} />
      <FaLinkedinIn className={"pa2 nb1 f4 black"} />
      <FaTwitter className={"pa2 nb1 f4 black"} />
      <FaWhatsapp className={"pa2 nb1 f4 black"} />
      <FaEllipsisH className={"pa2 nb1 f4 black"} />
    </button>
  </RWebShare>
);

export { SocialNetworkList };
