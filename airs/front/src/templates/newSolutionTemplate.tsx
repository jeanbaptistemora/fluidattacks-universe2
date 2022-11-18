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
/* eslint react/jsx-no-bind:0 */
/* eslint import/no-default-export:0 */
/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-namespace:0 */
import { graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import { ServiceSeo } from "../components/ServiceSeo";
import { SolutionPage } from "../scenes/SolutionPage";
import { PageArticle } from "../styles/styledComponents";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const NewSolutionIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { description, headtitle, identifier, image, keywords, slug, title } =
    data.markdownRemark.frontmatter;
  const { htmlAst } = data.markdownRemark;

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={image.replace(".webp", ".png")}
        keywords={keywords}
        title={
          headtitle
            ? `${headtitle} | Solutions | Fluid Attacks`
            : `${title} | Solutions | Fluid Attacks`
        }
        url={slug}
      />
      <ServiceSeo
        description={description}
        image={image.replace(".webp", ".png")}
        title={`${title} | Fluid Attacks`}
        url={`https://fluidattacks.com/${slug}`}
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
            <SolutionPage
              description={description}
              htmlAst={htmlAst}
              identifier={identifier}
              image={image}
              title={title}
            />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default NewSolutionIndex;

export const query: StaticQueryDocument = graphql`
  query NewSolutionIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      htmlAst
      fields {
        slug
      }
      frontmatter {
        banner
        description
        keywords
        slug
        identifier
        image
        title
        headtitle
      }
    }
  }
`;
