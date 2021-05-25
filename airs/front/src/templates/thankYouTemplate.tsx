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
  const { html } = data.asciidoc;
  const { title } = data.asciidoc.document;
  const { description, keywords, slug } = data.asciidoc.pageAttributes;

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
        keywords
      }
    }
  }
`;
