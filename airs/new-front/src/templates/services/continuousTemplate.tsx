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
/* eslint import/no-namespace:0 */
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import { Layout } from "../../components/layout";
import { NavbarComponent } from "../../components/navbar";
import React from "react";
import { Seo } from "../../components/seo";
import { graphql } from "gatsby";
import { translate } from "../../utils/translations/translate";
import {
  ArticleContainer,
  BannerContainer,
  BannerSubtitle,
  BannerTitle,
  FullWidthContainer,
  PageArticle,
  PageContainer,
} from "../../styles/styledComponents";

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

const ContinuousHackingIndex: React.FC<IQueryData> = ({
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
            <BannerContainer className={"bg-continuous"}>
              <FullWidthContainer>
                <BannerTitle>{title}</BannerTitle>
                <BannerSubtitle>
                  {translate.t("services.continuousHacking.subtitle")}
                </BannerSubtitle>
              </FullWidthContainer>
            </BannerContainer>
            <ArticleContainer>
              <PageContainer />
            </ArticleContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default ContinuousHackingIndex;

export const query: void = graphql`
  query ContinuousHackingIndex($slug: String!) {
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
      }
    }
  }
`;
