/* eslint import/no-default-export:0 */

import { graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import React, { useEffect } from "react";

import { Seo } from "../components/Seo";

const FreeTrialIndex: React.FC<IQueryData> = ({
  data,
}: IQueryData): JSX.Element => {
  useEffect((): void => {
    window.location.replace("https://app.fluidattacks.com/SignUp");
  });
  const { description, image, keywords, slug, title } =
    data.markdownRemark.frontmatter;

  return (
    <Seo
      description={description}
      image={image}
      keywords={keywords}
      title={`${title} | Fluid Attacks`}
      url={slug}
    />
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
