/* eslint import/no-default-export:0 */
import { graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { Seo } from "../components/Seo";
import { ServiceSeo } from "../components/ServiceSeo";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import { SolutionPage } from "../scenes/SolutionPage";
import { PageArticle } from "../styles/styledComponents";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const SolutionIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { description, headtitle, image, keywords, slug, title } =
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
              image={image}
              title={title}
            />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default SolutionIndex;

export const query: StaticQueryDocument = graphql`
  query SolutionIndex($slug: String!) {
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
