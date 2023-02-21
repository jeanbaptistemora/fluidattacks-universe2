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

import { PlansPage } from "../components/PlansPage";
import { Seo } from "../components/Seo";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import { PageArticle } from "../styles/styledComponents";

const PlansIndex: React.FC<IQueryData> = ({
  data,
}: IQueryData): JSX.Element => {
  const { description, keywords, slug, title } =
    data.markdownRemark.frontmatter;

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619635918/airs/clients/cover-clients_llnlaw.png"
        }
        keywords={keywords}
        title={`${title} | Fluid Attacks`}
        url={slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <PageArticle bgColor={"#f9f9f9"}>
            <PlansPage />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default PlansIndex;

export const query: StaticQueryDocument = graphql`
  query PlansIndex($slug: String!) {
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
