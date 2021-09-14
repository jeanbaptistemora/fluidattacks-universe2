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
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const MdCategoryIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const {
    banner,
    description,
    image,
    keywords,
    slug,
    defaux,
    definition,
    title,
  } = data.markdownRemark.frontmatter;

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={image.replace(".webp", ".png")}
        keywords={keywords}
        title={`${title} | Fluid Attacks`}
        url={slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={capitalizePlainString(title)}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
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
                        {definition}
                        <br />
                        <br />
                        {defaux}
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
                    __html: data.markdownRemark.html,
                  }}
                />
              </FullWidthContainer>
            </BigPageContainer>
            {slug === "categories/sast/" ? <SastPageFooter /> : undefined}
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default MdCategoryIndex;

export const query: void = graphql`
  query MdCategoryIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        description
        image
        banner
        defaux
        definition
        keywords
        slug
        title
      }
    }
  }
`;
