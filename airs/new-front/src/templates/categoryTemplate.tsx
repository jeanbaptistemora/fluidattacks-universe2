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
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { LanguagesList } from "../components/SastSupportedLanguages";
import { Seo } from "../components/Seo";
import {
  BannerContainer,
  BannerTitle,
  BlackH2,
  FullWidthContainer,
  PageArticle,
} from "../styles/styledComponents";

const CategoryIndex: React.FC<IQueryData> = ({
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
  const CategoryContainer: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
      roboto
      mw-1366
      ph-body
      center
      c-lightblack
      pv5
      compliance-page 
      flex 
      flex-wrap 
      items-center 
      justify-center
    `,
  })``;
  const CategoryContent: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
      solution-benefits
      justify-center
      items-center
      flex
      flex-wrap
    `,
  })``;
  const CategoryDefinition: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
      center
      roboto
      f3-l
      f4
      fw3
      lh-2
      pv4
    `,
  })``;

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
            <BannerContainer className={banner}>
              <FullWidthContainer>
                <BannerTitle>{title}</BannerTitle>
              </FullWidthContainer>
            </BannerContainer>
            <CategoryContainer>
              <CategoryDefinition>
                {data.asciidoc.pageAttributes.definition}
                <br />
                <br />
                {data.asciidoc.pageAttributes.defaux}
              </CategoryDefinition>
              <BlackH2 className={"roboto"}>{"Benefits"}</BlackH2>
              <CategoryContent
                dangerouslySetInnerHTML={{
                  __html: data.asciidoc.html,
                }}
              />
            </CategoryContainer>
            {data.asciidoc.pageAttributes.slug === "categories/sast/" ? (
              <LanguagesList />
            ) : undefined}
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default CategoryIndex;

export const query: void = graphql`
  query CategoryIndex($slug: String!) {
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
        defaux
        definition
        keywords
        slug
      }
    }
  }
`;
