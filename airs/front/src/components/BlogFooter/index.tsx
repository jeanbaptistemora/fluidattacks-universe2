/* eslint require-unicode-regexp:0 */
/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import { SocialNetworkList } from "./SocialNetworkList";
import {
  BlogFooterCols,
  BlogFooterColsBody,
  BlogFooterColsHeader,
  BlogFooterContainer,
  RedButton,
} from "./StyledComponents";

import { translate } from "../../utils/translations/translate";
import { CloudImage } from "../CloudImage";

interface IProps {
  author: string;
  slug: string;
  writer: string;
}

const BlogFooter: React.FC<IProps> = ({
  author,
  slug,
  writer,
}: IProps): JSX.Element => (
  <BlogFooterContainer>
    <BlogFooterCols>
      <BlogFooterColsHeader className={"ml2"}>
        {translate.t("blogFooter.authorHeader")}
      </BlogFooterColsHeader>
      <BlogFooterColsBody>
        <CloudImage
          alt={"Author picture"}
          src={`authors/${writer}`}
          styles={"w3 h3 br-100"}
        />
        <Link
          className={"arrow-box br3 pa2 ml3 mv1"}
          to={`/blog/authors/${author
            .toLowerCase()
            .replace(" ", "-")
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")}`}
        >
          {author}
        </Link>
      </BlogFooterColsBody>
    </BlogFooterCols>
    <BlogFooterCols>
      <BlogFooterColsHeader className={"ml1"}>
        {translate.t("blogFooter.shareHeader")}
      </BlogFooterColsHeader>
      <BlogFooterColsBody>
        <SocialNetworkList slug={slug} />
      </BlogFooterColsBody>
    </BlogFooterCols>
    <BlogFooterCols>
      <BlogFooterColsHeader>
        {translate.t("blogFooter.subscribeHeader")}
      </BlogFooterColsHeader>
      <BlogFooterColsBody>
        <Link
          className={"no-underline blog-suscribe-button mv1"}
          to={"/subscription/"}
        >
          <RedButton>{translate.t("blogFooter.subscribeButton")}</RedButton>
        </Link>
      </BlogFooterColsBody>
    </BlogFooterCols>
  </BlogFooterContainer>
);

export { BlogFooter };
