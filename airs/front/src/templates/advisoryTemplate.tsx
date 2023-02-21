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
/* eslint @typescript-eslint/no-unsafe-member-access: 0*/
/* eslint @typescript-eslint/no-unsafe-call: 0*/
/* eslint @typescript-eslint/no-explicit-any: 0*/

import { graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React, { createElement } from "react";
import rehypeReact from "rehype-react";

import { Seo } from "../components/Seo";
import { TimeLapse } from "../components/TimeLapse";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import {
  AdvisoryContainer,
  MarkedTitle,
  MarkedTitleContainer,
  PageArticle,
  RedMark,
} from "../styles/styledComponents";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const AdvisoryIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const renderAst = new (rehypeReact as any)({
    components: {
      "time-lapse": TimeLapse,
    },
    createElement,
  }).Compiler;

  const { description, headtitle, keywords, slug, title } =
    data.markdownRemark.frontmatter;
  const { htmlAst } = data.markdownRemark;

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619634447/airs/bg-advisories_htsqyd.png"
        }
        keywords={keywords}
        title={
          headtitle
            ? `${headtitle} | Advisories | Fluid Attacks`
            : `${title} | Advisories | Fluid Attacks`
        }
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

          <PageArticle bgColor={"#f4f4f6"}>
            <MarkedTitleContainer>
              <div className={"ph-body"}>
                <RedMark>
                  <MarkedTitle>{title}</MarkedTitle>
                </RedMark>
              </div>
            </MarkedTitleContainer>
            <AdvisoryContainer>{renderAst(htmlAst)}</AdvisoryContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default AdvisoryIndex;

export const query: StaticQueryDocument = graphql`
  query AdvisoryIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      htmlAst
      fields {
        slug
      }
      frontmatter {
        description
        keywords
        slug
        title
        headtitle
      }
    }
  }
`;
