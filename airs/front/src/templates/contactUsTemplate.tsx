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

const ContacUsIndex: React.FC<IQueryData> = ({
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
                  "https://forms.zohopublic.com/fluidattacks1/form/ContactForm/formperma/g4Je_6zumBrCA3iMMJMHU6b4JrVrUzItp_cfyb3ad74"
                }
                style={{
                  border: "0",
                  height: "1000px",
                  marginBottom: "-7px",
                  width: "100%",
                }}
                title={"Contact Us Form"}
              />
            </IframeContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default ContacUsIndex;

export const query: StaticQueryDocument = graphql`
  query ContactUsIndex($slug: String!) {
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
