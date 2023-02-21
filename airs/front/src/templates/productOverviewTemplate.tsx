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
import type { StaticQueryDocument } from "gatsby";
import { decode } from "he";
import React from "react";

import { ProductOverviewPage } from "../components/ProductOverviewPage";
import { Seo } from "../components/Seo";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";

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
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1669230787/airs/logo-fluid-2022.png"
        }
        keywords={keywords}
        title={decode(`${title} | Fluid Attacks`)}
        url={slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <ProductOverviewPage description={description} />
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default ProductOverview;

export const query: StaticQueryDocument = graphql`
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
