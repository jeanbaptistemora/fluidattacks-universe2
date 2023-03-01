/* eslint react/no-danger:0 */
/* eslint import/no-default-export:0 */
/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import React from "react";

import { Breadcrumbs } from "../components/Breadcrumbs";
import { PageHeader } from "../components/PageHeader";
import { Seo } from "../components/Seo";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import { IframeContainer, PageArticle } from "../styles/styledComponents";

const SubscribeIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const { location } = pageContext.breadcrumb;

  const home = ["/"];
  const path = home.concat(
    location.split("/").filter((name): boolean => name !== "")
  );

  const { description, keywords, slug, subtext, subtitle, title } =
    data.markdownRemark.frontmatter;

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619631770/airs/contact-us/bg-contact-us_cpcyoj.png"
        }
        keywords={keywords}
        title={`${title} | Fluid Attacks`}
        url={slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumbs currentPath={path} />

          <PageArticle bgColor={"#f9f9f9"}>
            <PageHeader
              banner={"contact-bg"}
              pageWithBanner={true}
              slug={slug}
              subtext={subtext}
              subtitle={subtitle}
              title={title}
            />

            <IframeContainer>
              <iframe
                sandbox={
                  "allow-forms allow-top-navigation allow-same-origin allow-scripts allow-popups"
                }
                src={
                  "https://forms.zohopublic.com/fluidattacks1/form/Newsletter/formperma/Oj1qU25E49Iy6up1YnEtxsXuOxqbDEl1V5QtvLIAM7c"
                }
                style={{
                  border: "0",
                  height: "700px",
                  width: "100%",
                }}
                title={"Suscription form"}
              />
            </IframeContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default SubscribeIndex;

export const query: StaticQueryDocument = graphql`
  query SubscribeIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      fields {
        slug
      }
      frontmatter {
        description
        keywords
        title
      }
    }
  }
`;
