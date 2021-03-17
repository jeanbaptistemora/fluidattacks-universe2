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
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import { Layout } from "../components/layout";
import { NavbarComponent } from "../components/navbar";
import { PageHeader } from "../components/PageHeader";
import React from "react";
import { Seo } from "../components/seo";
import { graphql } from "gatsby";
import {
  ArticleContainer,
  ArticleTitle,
  PageArticle,
} from "../styles/styledComponents";

const DefaultPage: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { title } = data.asciidoc.document;
  const customCrumbLabel: string = `${title
    .charAt(0)
    .toUpperCase()}${title.slice(1).replace("-", "")}`;

  const hasBanner: boolean =
    typeof data.asciidoc.pageAttributes.banner === "string";
  const isCareers: boolean = data.asciidoc.pageAttributes.slug === "careers/";

  return (
    <React.Fragment>
      <Seo
        description={data.asciidoc.pageAttributes.description}
        keywords={data.asciidoc.pageAttributes.keywords}
        title={`${title} | Fluid Attacks`}
        url={data.asciidoc.pageAttributes.slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={customCrumbLabel}
            crumbSeparator={" / "}
            crumbs={crumbs}
          />

          <PageArticle>
            <PageHeader
              banner={data.asciidoc.pageAttributes.banner}
              pageWithBanner={hasBanner}
              slug={data.asciidoc.pageAttributes.slug}
              subtext={data.asciidoc.pageAttributes.subtext}
              subtitle={data.asciidoc.pageAttributes.subtitle}
              title={title}
            />
            {isCareers ? <ArticleTitle>{title}</ArticleTitle> : undefined}
            <ArticleContainer
              className={"internal"}
              dangerouslySetInnerHTML={{
                __html: data.asciidoc.html,
              }}
            />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default DefaultPage;

export const query: void = graphql`
  query PageArticleBySlug($slug: String!) {
    asciidoc(fields: { slug: { eq: $slug } }) {
      document {
        title
      }
      html
      fields {
        slug
      }
      pageAttributes {
        banner
        description
        keywords
        slug
        subtext
        subtitle
      }
    }
  }
`;
