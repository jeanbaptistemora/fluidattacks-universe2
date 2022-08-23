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
import { graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { FloatingButton } from "../components/FloatingButton";
import { InternalForm } from "../components/InternalForm";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import { ServiceSeo } from "../components/ServiceSeo";
import { Paragraph } from "../components/Texts";
import {
  BigPageContainer,
  BlackH2,
  MarkedTitle,
  PageArticle,
  RedMark,
  ServicesGrid,
  ServicesHeaderContainer,
} from "../styles/styledComponents";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const ContinuousHackingIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { description, image, keywords, slug, subtext, title } =
    data.markdownRemark.frontmatter;

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={image}
        keywords={keywords}
        title={`${title} | Fluid Attacks`}
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
          <Breadcrumb
            crumbLabel={capitalizePlainString(title)}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

          <PageArticle bgColor={"#f9f9f9"}>
            <BigPageContainer>
              <ServicesHeaderContainer>
                <RedMark>
                  <MarkedTitle>{title}</MarkedTitle>
                </RedMark>
                <Paragraph fColor={"#2e2e38"} fSize={"16"} maxWidth={"1864"}>
                  {subtext}
                </Paragraph>
              </ServicesHeaderContainer>
              <BlackH2>{"Key Features"}</BlackH2>
              <ServicesGrid
                dangerouslySetInnerHTML={{
                  __html: data.markdownRemark.html,
                }}
              />
            </BigPageContainer>
            <InternalForm />
            <FloatingButton
              bgColor={"#2e2e38"}
              color={"#fff"}
              text={"Start free trial"}
              to={"/free-trial/"}
              yPosition={"50%"}
            />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default ContinuousHackingIndex;

export const query: StaticQueryDocument = graphql`
  query ServiceIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        banner
        description
        keywords
        slug
        subtext
        image
        title
      }
    }
  }
`;
