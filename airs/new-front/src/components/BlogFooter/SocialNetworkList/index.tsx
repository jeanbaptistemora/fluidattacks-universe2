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
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

interface IProps {
  slug: string;
}
const SocialListContainer: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
      c-fluid-bk
      fw4
      f-1125
      dib-l
      v-mid
      mh4-l
      pv0-l
      pv3
    `,
})``;
const SocialNetworkList: React.FC<IProps> = ({ slug }: IProps): JSX.Element => (
  <SocialListContainer>
    {"Share:"}
    <TwitterShareButton
      title={"Share on Twitter"}
      url={`https://fluidattacks.com/${slug}`}
    >
      <FontAwesomeIcon className={"f4 mh2 c-fluid-gray"} icon={faTwitter} />
    </TwitterShareButton>
    <FacebookShareButton
      title={"Share on Facebook"}
      url={`https://fluidattacks.com/${slug}`}
    >
      <FontAwesomeIcon className={"f4 mh2 c-fluid-gray"} icon={faFacebookF} />
    </FacebookShareButton>
    <LinkedinShareButton
      title={"Share on LinkedIn"}
      url={`https://fluidattacks.com/${slug}`}
    >
      <FontAwesomeIcon className={"f4 mh2 c-fluid-gray"} icon={faLinkedinIn} />
    </LinkedinShareButton>
  </SocialListContainer>
);

export { SocialNetworkList };
