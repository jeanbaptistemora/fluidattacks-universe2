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
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { Seo } from "../components/Seo";
import { ServicesPage } from "../components/ServicesPage";
import { Title } from "../components/Texts";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import { PageArticle, SectionContainer } from "../styles/styledComponents";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const ServicesIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { description, image, keywords, slug, title } =
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

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={capitalizePlainString(title)}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

          <PageArticle bgColor={"#f4f4f6"}>
            <SectionContainer>
              <Title fColor={"#2e2e38"} fSize={"48"}>
                {title}
              </Title>
              <ServicesPage />
            </SectionContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default ServicesIndex;

export const query: StaticQueryDocument = graphql`
  query ServicesIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        keywords
        description
        slug
        title
        image
      }
    }
  }
`;
