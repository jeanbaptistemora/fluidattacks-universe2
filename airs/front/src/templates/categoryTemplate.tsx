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
import type { StaticQueryDocument } from "gatsby";
import React from "react";

import { Breadcrumbs } from "../components/Breadcrumbs";
import { SastPageFooter } from "../components/SastPageFooter";
import { Seo } from "../components/Seo";
import { ServiceSeo } from "../components/ServiceSeo";
import { Paragraph } from "../components/Texts";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import {
  BlackH2,
  ComplianceContainer,
  FlexCenterItemsContainer,
  FullWidthContainer,
  MarkedTitle,
  PageArticle,
  RedMark,
} from "../styles/styledComponents";

const CategoryIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const { location } = pageContext.breadcrumb;

  const home = ["/"];
  const path = home.concat(
    location.split("/").filter((name): boolean => name !== "")
  );

  const {
    description,
    headtitle,
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
        title={
          headtitle
            ? `${headtitle} | Products | Fluid Attacks`
            : `${title} | Products | Fluid Attacks`
        }
        url={slug}
      />
      <ServiceSeo
        description={description}
        image={image.replace(".webp", ".png")}
        title={`${title} | Fluid Attacks`}
        url={`https://fluidattacks.com/${slug}`}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumbs currentPath={path} />

          <PageArticle bgColor={"#f9f9f9"}>
            <ComplianceContainer>
              <RedMark>
                <MarkedTitle>{title}</MarkedTitle>
              </RedMark>
              <Paragraph fColor={"#2e2e38"} fSize={"16"} marginTop={"1"}>
                {definition}
              </Paragraph>
              <Paragraph fColor={"#2e2e38"} fSize={"16"} marginTop={"1"}>
                {defaux}
              </Paragraph>
              <FullWidthContainer>
                <BlackH2>{`These are the benefits of ${title}`}</BlackH2>
                <FlexCenterItemsContainer
                  className={"solution-benefits flex-wrap"}
                  dangerouslySetInnerHTML={{
                    __html: data.markdownRemark.html,
                  }}
                />
              </FullWidthContainer>
              {slug === "product/sast/" ? <SastPageFooter /> : undefined}
            </ComplianceContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default CategoryIndex;

export const query: StaticQueryDocument = graphql`
  query CategoryIndex($slug: String!) {
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
        headtitle
      }
    }
  }
`;
