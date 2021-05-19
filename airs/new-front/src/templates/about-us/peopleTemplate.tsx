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
import { graphql } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { Layout } from "../../components/Layout";
import { NavbarComponent } from "../../components/Navbar";
import { PeopleSectionList } from "../../components/PeopleSectionsList";
import { Seo } from "../../components/Seo";
import {
  ArticleContainer,
  BannerTitle,
  FullWidthContainer,
  LittleBannerContainer,
  PageArticle,
} from "../../styles/styledComponents";

const PeopleIndex: React.FC<IQueryData> = ({
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

  const { banner } = data.asciidoc.pageAttributes;

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
            <LittleBannerContainer className={banner}>
              <FullWidthContainer>
                <BannerTitle>{title}</BannerTitle>
              </FullWidthContainer>
            </LittleBannerContainer>
            <ArticleContainer>
              <PeopleSectionList />
            </ArticleContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default PeopleIndex;

export const query: void = graphql`
  query PeoplePage($slug: String!) {
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
