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
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import {
  ComplianceContainer,
  MarkedTitle,
  PageArticle,
  RedMark,
} from "../styles/styledComponents";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const SystemIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { description, headtitle, keywords, slug, title } =
    data.markdownRemark.frontmatter;

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619637249/airs/compliance/cover-internal-compliance_clerwf.png"
        }
        keywords={keywords}
        title={
          headtitle
            ? `${headtitle} | Systems | Fluid Attacks`
            : `${title} | Systems | Fluid Attacks`
        }
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
            <ComplianceContainer>
              <RedMark>
                <MarkedTitle>{title}</MarkedTitle>
              </RedMark>
              <div
                dangerouslySetInnerHTML={{
                  __html: data.markdownRemark.html,
                }}
              />
            </ComplianceContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default SystemIndex;

export const query: StaticQueryDocument = graphql`
  query SystemIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        description
        keywords
        slug
        title
        headtitle
      }
    }
  }
`;
