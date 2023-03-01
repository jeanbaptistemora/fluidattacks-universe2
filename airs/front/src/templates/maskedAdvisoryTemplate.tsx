/* eslint import/no-default-export:0 */
/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint @typescript-eslint/no-unsafe-member-access: 0*/
/* eslint @typescript-eslint/no-unsafe-call: 0*/
/* eslint @typescript-eslint/no-explicit-any: 0*/
/* eslint @typescript-eslint/restrict-template-expressions: 0*/

import { useAuth0, withAuthenticationRequired } from "@auth0/auth0-react";
import type { Auth0ContextInterface } from "@auth0/auth0-react";
import { graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import React, { createElement } from "react";
import rehypeReact from "rehype-react";

import { Breadcrumbs } from "../components/Breadcrumbs";
import { LogoutButton } from "../components/LogoutButton";
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

const MaskedAdvisoryIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const { location } = pageContext.breadcrumb;

  const home = ["/"];
  const path = home.concat(
    location.split("/").filter((name): boolean => name !== "")
  );

  const renderAst = new (rehypeReact as any)({
    components: {
      "time-lapse": TimeLapse,
    },
    createElement,
  }).Compiler;

  const { description, keywords, slug, title } =
    data.markdownRemark.frontmatter;
  const { htmlAst } = data.markdownRemark;
  const { user }: Auth0ContextInterface = useAuth0();

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619634447/airs/bg-advisories_htsqyd.png"
        }
        keywords={keywords}
        title={`${title} | Fluid Attacks`}
        url={slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumbs currentPath={path} />

          <PageArticle bgColor={"#f4f4f6"}>
            <p>{`Logged in as: ${user?.email}`}</p>
            <LogoutButton />
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

export default withAuthenticationRequired(MaskedAdvisoryIndex);

export const query: StaticQueryDocument = graphql`
  query MaskedAdvisoryIndex($slug: String!) {
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
      }
    }
  }
`;
