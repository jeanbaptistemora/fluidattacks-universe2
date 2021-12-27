/* eslint import/no-default-export:0 */
/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { graphql } from "gatsby";
import React from "react";

import { Seo } from "../components/Seo";
import { ThankYouContent } from "../components/ThankYouContent";

const SubscribeIndex: React.FC<IQueryData> = ({
  data,
}: IQueryData): JSX.Element => {
  const { html } = data.markdownRemark;
  const { description, keywords, slug, title } =
    data.markdownRemark.frontmatter;

  return (
    <React.Fragment>
      <Seo
        description={description}
        keywords={keywords}
        title={`${title} | Fluid Attacks`}
        url={slug}
      />

      <ThankYouContent content={html} title={title} />
    </React.Fragment>
  );
};

export default SubscribeIndex;

export const query: void = graphql`
  query ThankYouIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        description
        keywords
        title
      }
    }
  }
`;
