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
import React from "react";
import { Seo } from "../components/seo";
import { graphql } from "gatsby";
import {
  ArticleContainer,
  BannerContainer,
  BannerInnerContainer,
  BannerTitle,
  PageArticle,
} from "../styles/styledComponents";
import "../assets/scss/index.scss";

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
        banner?: string;
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

const SolutionsIndex: React.FC<IQueryData> = ({
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

  const banner: string = data.asciidoc.pageAttributes.banner as string;

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
            <BannerContainer className={banner}>
              <BannerInnerContainer>
                <BannerTitle>{title}</BannerTitle>
              </BannerInnerContainer>
            </BannerContainer>
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

export default SolutionsIndex;

export const query: void = graphql`
  query PageArticle($slug: String!) {
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
        banner
      }
    }
  }
`;
