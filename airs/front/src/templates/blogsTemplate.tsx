/*
 *There is no danger using dangerouslySetInnerHTML since everything is built in
 *compile time, also
 *Default exports are needed for pages used in nodes by default to create pages
 *like index.tsx or this one
 */
/* eslint react/no-danger:0 */
/* eslint import/no-default-export:0 */
/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
import { Link, graphql } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import { decode } from "he";
import { utc } from "moment";
import React from "react";

import { BlogFooter } from "../components/BlogFooter";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import {
  BlogArticleBannerContainer,
  BlogArticleContainer,
  BlogArticleSubtitle,
  BlogArticleTitle,
  FullWidthContainer,
  PageArticle,
} from "../styles/styledComponents";
import {
  capitalizeDashedString,
  capitalizeObject,
  capitalizePlainString,
  stringToUri,
} from "../utils/utilities";

const BlogsIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const {
    alt,
    author,
    category,
    date,
    description,
    image,
    keywords,
    slug,
    subtitle,
    tags,
    title,
    writer,
  } = data.markdownRemark.frontmatter;
  const taglist: string[] = tags.split(", ");
  const fDate = utc(date.toLocaleString()).format("LL");

  return (
    <React.Fragment>
      <Seo
        author={author}
        description={description}
        image={image.replace(".webp", ".png")}
        keywords={keywords}
        title={`${decode(title)} | Fluid Attacks`}
        url={slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={decode(capitalizePlainString(title))}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

          <PageArticle className={"internal"}>
            <BlogArticleBannerContainer>
              <FullWidthContainer>
                <div className={"w-100"}>
                  <img alt={alt} className={"w-100 db"} src={image} />
                </div>
              </FullWidthContainer>
            </BlogArticleBannerContainer>
            <BlogArticleContainer>
              <BlogArticleTitle>{decode(title)}</BlogArticleTitle>
              <BlogArticleSubtitle>{decode(subtitle)}</BlogArticleSubtitle>
              <div className={"pv3"}>
                <p className={"f5"}>
                  {"By"}&nbsp;
                  <Link to={`/blog/authors/${stringToUri(author)}`}>
                    {author}
                  </Link>
                  {` | ${fDate} | `}
                  <Link to={"/blog/categories/"}>{"Category:"}</Link>{" "}
                  <Link to={`/blog/categories/${category.toLocaleLowerCase()}`}>
                    {capitalizeDashedString(category)}
                  </Link>
                </p>
              </div>
              <div
                className={"lh-2"}
                dangerouslySetInnerHTML={{
                  __html: data.markdownRemark.html,
                }}
              />
              <div className={"pt3"}>
                <p className={"f5"}>
                  <Link to={"/blog/tags/"}>{"Tags:"}</Link>
                  {taglist.map(
                    (tag: string, index): JSX.Element =>
                      taglist.length === index + 1 ? (
                        <Link
                          className={
                            "ph2 mh2 mb2 dib hv-fluid-rd button-white br2"
                          }
                          to={`/blog/tags/${tag}`}
                        >
                          {capitalizeDashedString(tag)}
                        </Link>
                      ) : (
                        <Link
                          className={
                            "ph2 mh2 mb2 dib hv-fluid-rd button-white br2"
                          }
                          to={`/blog/tags/${tag}`}
                        >
                          {capitalizeDashedString(tag)}
                        </Link>
                      )
                  )}
                </p>
              </div>
              <BlogFooter author={author} slug={slug} writer={writer} />
            </BlogArticleContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default BlogsIndex;

export const query: void = graphql`
  query BlogsPages($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        alt
        author
        category
        date
        description
        image
        keywords
        slug
        subtitle
        tags
        writer
        title
      }
    }
  }
`;
