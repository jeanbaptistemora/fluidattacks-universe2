/*
 *There is no danger using dangerouslySetInnerHTML since everything is built in
 *compile time, also
 *Default exports are needed for pages used in nodes by default to create pages
 *like index.tsx or this one
 */
/* eslint react/no-danger:0 */
/* eslint react/jsx-no-bind:0 */
/* eslint import/no-default-export:0 */
/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint @typescript-eslint/no-unsafe-member-access: 0*/
/* eslint @typescript-eslint/no-unsafe-call: 0*/
/* eslint @typescript-eslint/no-explicit-any: 0*/
import { graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import { decode } from "he";
import { utc } from "moment";
import React from "react";

import { BlogSeo } from "../components/BlogSeo";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import { BlogPage } from "../scenes/BlogPage";
import { PageArticle } from "../styles/styledComponents";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const BlogsIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { htmlAst } = data.markdownRemark;

  const {
    author,
    category,
    date,
    definition,
    description,
    headtitle,
    image,
    keywords,
    modified,
    slug,
    subtitle,
    tags,
    title,
    writer,
  } = data.markdownRemark.frontmatter;
  const fDate = utc(new Date(date)).format("LL");

  return (
    <React.Fragment>
      <Seo
        author={author}
        description={description}
        image={image.replace(".webp", ".png")}
        keywords={keywords}
        title={
          headtitle
            ? `${decode(headtitle)} | Blog | Fluid Attacks`
            : `${decode(title)} | Blog | Fluid Attacks`
        }
        url={`https://fluidattacks.com/blog/${slug}`}
      />
      <BlogSeo
        author={author}
        date={fDate}
        dateModified={
          modified ? utc(modified.toLocaleString()).format("LL") : fDate
        }
        description={description}
        image={image.replace(".webp", ".pn g")}
        title={`${decode(title)} | Fluid Attacks`}
        url={`https://fluidattacks.com/blog/${slug}`}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={decode(capitalizePlainString(title))}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

          <PageArticle bgColor={"#fff"}>
            <BlogPage
              author={author}
              category={category}
              date={fDate}
              description={definition}
              htmlAst={htmlAst}
              image={image}
              slug={slug}
              subtitle={subtitle}
              tags={tags}
              title={title}
              writer={writer}
            />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default BlogsIndex;

export const query: StaticQueryDocument = graphql`
  query BlogsPages($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      htmlAst
      fields {
        slug
      }
      frontmatter {
        alt
        author
        category
        date
        definition
        modified
        description
        image
        keywords
        slug
        subtitle
        tags
        writer
        title
        headtitle
      }
    }
  }
`;
