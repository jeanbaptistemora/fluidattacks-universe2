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
import { decode } from "he";
import React from "react";

import { Layout } from "../components/Layout";
import { ProductOverviewPage } from "../components/ProductOverviewPage";
import { Seo } from "../components/Seo";

const ProductOverview: React.FC<IQueryData> = ({
  data,
}: IQueryData): JSX.Element => {
  const { description, keywords, slug, title } =
    data.markdownRemark.frontmatter;

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/c_scale,w_1200/v1622583388/airs/logo_fluid_attacks_2021_eqop3k.png"
        }
        keywords={keywords}
        title={decode(`${title} | Fluid Attacks`)}
        url={slug}
      />

      <Layout>
        <ProductOverviewPage description={description} />
      </Layout>
    </React.Fragment>
  );
};

export default ProductOverview;

export const query: void = graphql`
  query ProductOverviewBySlug($slug: String!) {
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
      }
    }
  }
`;
