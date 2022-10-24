/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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

import { BlogSeo } from "../components/BlogSeo";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { ResourcesPage } from "../components/ResourcesPage";
import { Seo } from "../components/Seo";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const ResourcesIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { description, keywords, slug, title } =
    data.markdownRemark.frontmatter;

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619632049/airs/resources/resources-main_u1gggc.png"
        }
        keywords={keywords}
        title={`${title} | Fluid Attacks`}
        url={slug}
      />
      <BlogSeo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619632049/airs/resources/resources-main_u1gggc.png"
        }
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
          <ResourcesPage bannerTitle={title} />
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default ResourcesIndex;

export const query: StaticQueryDocument = graphql`
  query ResourcesIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        keywords
        phrase
        slug
        title
      }
    }
  }
`;
