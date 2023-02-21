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

import { FreeTrialPage } from "../components/FreeTrialPage";
import { Seo } from "../components/Seo";
import { Layout } from "../scenes/Footer/Layout";
import { PageArticle } from "../styles/styledComponents";

const FreeTrialIndex: React.FC<IQueryData> = ({
  data,
}: IQueryData): JSX.Element => {
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
          <PageArticle bgColor={"#f4f4f6"}>
            <FreeTrialPage />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default FreeTrialIndex;

export const query: StaticQueryDocument = graphql`
  query FreeTrialIndex($slug: String!) {
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
