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
/* eslint require-unicode-regexp:0 */
import { Link, graphql } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import { decode } from "he";
import moment from "moment";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { BlogFooter } from "../components/BlogFooter";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import { FullWidthContainer, PageArticle } from "../styles/styledComponents";
import { capitalizeCrumbs } from "../utils/capitalizeCrumbs";

const BlogsIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { title } = data.asciidoc.document;
  const fDate = moment(data.asciidoc.pageAttributes.date).format(
    "MMMM DD, YYYY"
  );
  const customCrumbLabel: string = `${title
    .charAt(0)
    .toUpperCase()}${title.slice(1).replace("-", "")}`;
  const ArticleBannerContainer: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
      coverm
      cover-s
      h-auto
      justify-center
      items-center
      flex
      bg-center
      mw-900
      ml-auto
      mr-auto
    `,
  })``;
  const ArticleContainer: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
      roboto
      internal
      mw-900
      ml-auto
      mr-auto
      roboto
      bg-white
      ph4-l
      ph3
      pt4
      pb5
    `,
  })``;
  const ArticleTitle: StyledComponent<
    "h1",
    Record<string, unknown>
  > = styled.h1.attrs({
    className: `
      roboto
      tc
    `,
  })``;
  const ArticleSubtitle: StyledComponent<
    "span",
    Record<string, unknown>
  > = styled.span.attrs({
    className: `
      db
      tc c-fluid-bk
      b
      f3
      mt0
    `,
  })``;

  const authorUrl: string = data.asciidoc.pageAttributes.author
    .toLowerCase()
    .replace(" ", "-")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");

  return (
    <React.Fragment>
      <Seo
        description={data.asciidoc.pageAttributes.description}
        image={data.asciidoc.pageAttributes.image}
        keywords={data.asciidoc.pageAttributes.keywords}
        title={`${decode(title)} | Fluid Attacks`}
        url={data.asciidoc.pageAttributes.slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={decode(customCrumbLabel)}
            crumbSeparator={" / "}
            crumbs={capitalizeCrumbs(crumbs)}
          />

          <PageArticle className={"internal"}>
            <ArticleBannerContainer>
              <FullWidthContainer>
                <div className={"w-100"}>
                  <img
                    alt={data.asciidoc.pageAttributes.alt}
                    className={"w-100 db"}
                    src={data.asciidoc.pageAttributes.image}
                  />
                </div>
              </FullWidthContainer>
            </ArticleBannerContainer>
            <ArticleContainer>
              <ArticleTitle>{decode(title)}</ArticleTitle>
              <ArticleSubtitle>
                {decode(data.asciidoc.pageAttributes.subtitle)}
              </ArticleSubtitle>
              <div className={"pv3"}>
                <p className={"f5"}>
                  {"By"}&nbsp;
                  <Link to={`/blog/authors/${authorUrl}`}>
                    {data.asciidoc.pageAttributes.author}
                  </Link>
                  {` | ${fDate}`}
                </p>
              </div>
              <div
                className={"lh-2"}
                dangerouslySetInnerHTML={{
                  __html: data.asciidoc.html,
                }}
              />
              <BlogFooter
                author={data.asciidoc.pageAttributes.author}
                slug={data.asciidoc.pageAttributes.slug}
                writer={data.asciidoc.pageAttributes.writer}
              />
            </ArticleContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default BlogsIndex;

export const query: void = graphql`
  query BlogsPages($slug: String!) {
    asciidoc(fields: { slug: { eq: $slug } }) {
      document {
        title
      }
      html
      fields {
        slug
      }
      pageAttributes {
        alt
        author
        date
        description
        image
        keywords
        slug
        subtitle
        writer
      }
    }
  }
`;
