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
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import { Layout } from "../components/layout";
import { NavbarComponent } from "../components/navbar";
import React from "react";
import { Seo } from "../components/seo";
import { graphql } from "gatsby";
import {
  ArticleContainer,
  ArticleTitle,
  PageArticle,
} from "../styles/styledComponents";

import "tachyons/css/tachyons.min.css";
import "../styles/index.scss";

interface IQueryData {
  data: {
    asciidoc: {
      document: {
        title: string;
      };
      html: string;
      fields: {
        slug: string;
      };
      pageAttributes: {
        description: string;
        keywords: string;
        slug: string;
      };
    };
  };
  pageContext: {
    breadcrumb: {
      location: string;
      crumbs: [
        {
          pathname: string;
          crumbLabel: string;
        }
      ];
    };
    slug: string;
  };
}

const DefaultPage: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const title: string = data.asciidoc.document.title;
  const customCrumbLabel: string = `${title
    .charAt(0)
    .toUpperCase()}${title.slice(1).replace("-", "")}`;

  return (
    <React.Fragment>
      <Seo
        description={data.asciidoc.pageAttributes.description}
        keywords={data.asciidoc.pageAttributes.keywords}
        title={title}
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
            <ArticleTitle>{title}</ArticleTitle>
            <ArticleContainer
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
        description
        keywords
        slug
      }
    }
  }
`;
