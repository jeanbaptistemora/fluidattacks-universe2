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
import { graphql } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import {
  CompliancesGrid,
  MarkedPhrase,
  MarkedTitle,
  MarkedTitleContainer,
  RedMark,
} from "../styles/styledComponents";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const CompliancesIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const {
    description,
    keywords,
    phrase,
    slug,
    title,
  } = data.markdownRemark.frontmatter;

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619637251/airs/compliance/cover-compliance_vnojb7.png"
        }
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
          <MarkedTitleContainer>
            <div className={"pl4"}>
              <RedMark>
                <MarkedTitle>{title}</MarkedTitle>
              </RedMark>
              <MarkedPhrase>{phrase}</MarkedPhrase>
            </div>
            <CompliancesGrid
              dangerouslySetInnerHTML={{
                __html: data.markdownRemark.html,
              }}
            />
          </MarkedTitleContainer>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default CompliancesIndex;

export const query: void = graphql`
  query CompliancesIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        description
        banner
        keywords
        phrase
        slug
        title
      }
    }
  }
`;
