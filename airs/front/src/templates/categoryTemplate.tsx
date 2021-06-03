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

import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { SastPageFooter } from "../components/SastPageFooter";
import { Seo } from "../components/Seo";
import {
  BannerContainer,
  BigPageContainer,
  BlackH2,
  FlexCenterItemsContainer,
  FullWidthContainer,
  LittleBannerTitle,
  LittleBlackParagraph,
  PageArticle,
  PageContainer,
} from "../styles/styledComponents";
import { capitalizeCrumbs } from "../utils/capitalizeCrumbs";

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

  return (
    <React.Fragment>
      <Seo
        description={data.asciidoc.pageAttributes.description}
        image={data.asciidoc.pageAttributes.image}
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
            crumbs={capitalizeCrumbs(crumbs)}
          />

          <PageArticle>
            <BannerContainer className={banner}>
              <FullWidthContainer>
                <LittleBannerTitle>{title}</LittleBannerTitle>
              </FullWidthContainer>
            </BannerContainer>
            <PageContainer>
              <FullWidthContainer className={"pv4"}>
                <FlexCenterItemsContainer className={"flex-wrap center"}>
                  <div>
                    <div className={"tl"}>
                      <LittleBlackParagraph className={"tl"}>
                        {data.asciidoc.pageAttributes.definition}
                        <br />
                        <br />
                        {data.asciidoc.pageAttributes.defaux}
                      </LittleBlackParagraph>
                    </div>
                  </div>
                </FlexCenterItemsContainer>
              </FullWidthContainer>
            </PageContainer>
            <BigPageContainer>
              <FullWidthContainer className={"pv4"}>
                <BlackH2 className={"roboto"}>{"Benefits"}</BlackH2>
                <FlexCenterItemsContainer
                  className={"solution-benefits flex-wrap"}
                  dangerouslySetInnerHTML={{
                    __html: data.asciidoc.html,
                  }}
                />
              </FullWidthContainer>
            </BigPageContainer>
            {data.asciidoc.pageAttributes.slug === "categories/sast/" ? (
              <SastPageFooter />
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
        description
        image
        banner
        defaux
        definition
        keywords
        slug
      }
    }
  }
`;
