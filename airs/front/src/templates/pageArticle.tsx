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
/* eslint fp/no-mutation: 0 */
/* eslint react/forbid-component-props: 0 */
import { graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import { decode } from "he";
import React from "react";

import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { PageHeader } from "../components/PageHeader";
import { Seo } from "../components/Seo";
import {
  ArticleContainer,
  ArticleTitle,
  PageArticle,
} from "../styles/styledComponents";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const MdDefaultPage: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { banner, description, keywords, slug, subtext, subtitle, title } =
    data.markdownRemark.frontmatter;

  const hasBanner: boolean = typeof banner === "string";
  const isCareers: boolean = slug === "careers/";

  const isComparative: boolean = slug === "services/comparative/";
  const serviceIndex = crumbs.findIndex(
    (crumb): boolean => crumb.crumbLabel === "services"
  );

  const changeCrumbs = (
    index: number
  ): [{ pathname: string; crumbLabel: string }] => {
    const comparativeCrumbs = crumbs;
    comparativeCrumbs[index].pathname = "/services/continuous-hacking/";

    return comparativeCrumbs;
  };

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
          <Breadcrumb
            crumbLabel={decode(capitalizePlainString(title))}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(
              isComparative ? changeCrumbs(serviceIndex) : crumbs
            )}
          />

          <PageArticle bgColor={"#f9f9f9"}>
            <PageHeader
              banner={banner}
              pageWithBanner={hasBanner}
              slug={slug}
              subtext={subtext}
              subtitle={subtitle}
              title={decode(title)}
            />
            {isCareers ? (
              <ArticleTitle>{decode(title)}</ArticleTitle>
            ) : undefined}
            <ArticleContainer
              className={"internal"}
              dangerouslySetInnerHTML={{
                __html: data.markdownRemark.html,
              }}
            />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default MdDefaultPage;

export const query: StaticQueryDocument = graphql`
  query PageArticleBySlug($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        banner
        description
        keywords
        slug
        subtext
        title
        subtitle
      }
    }
  }
`;
