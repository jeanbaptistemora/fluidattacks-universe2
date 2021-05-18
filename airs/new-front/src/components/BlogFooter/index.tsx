/* eslint react/forbid-component-props: 0 */
import { faArrowRight } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "gatsby";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { SocialNetworkList } from "./SocialNetworkList";

import { CloudImage } from "../CloudImage";

interface IProps {
  author: string;
  slug: string;
  writer: string;
}

const BlogFooterContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
      w-100
      tl
      pt6-l
      pt5
      mw6-m
      ml-auto
      mr-auto
    `,
})``;
const ShareSection: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
      dib-l
      tl
      v-top
      ph3-l
      pv4-l
    `,
})``;
const AuthorTitle: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
      c-fluid-bk
      fw4
      f-1125
      dib-l
      v-mid
      mr4-l
      pv0-l
      pv3
    `,
})``;
const SuscribeContainer: StyledComponent<
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
      pt0-l
      pt4
    `,
})``;

const BlogFooter: React.FC<IProps> = ({
  author,
  slug,
  writer,
}: IProps): JSX.Element => (
  <BlogFooterContainer>
    <CloudImage
      alt={"Author picture"}
      src={`authors/${writer}`}
      styles={"w4 br-100 dib-l"}
    />
    <ShareSection>
      <AuthorTitle>{author}</AuthorTitle>
      <SocialNetworkList slug={slug} />
      <SuscribeContainer>
        <Link className={"sub-btn f3"} to={"/subscription/"}>
          {"Subscribe Now "}
          <FontAwesomeIcon className={"f4 c-hovered-red"} icon={faArrowRight} />
        </Link>
      </SuscribeContainer>
    </ShareSection>
  </BlogFooterContainer>
);

export { BlogFooter };
