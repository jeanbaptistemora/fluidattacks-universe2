/* eslint react/no-danger:0 */
/* eslint import/no-default-export:0 */
/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { graphql } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { PageHeader } from "../components/PageHeader";
import { Seo } from "../components/Seo";
import { IframeContainer, PageArticle } from "../styles/styledComponents";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const SubscribeIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const {
    description,
    keywords,
    slug,
    subtext,
    subtitle,
    title,
  } = data.markdownRemark.frontmatter;

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
          <Breadcrumb
            crumbLabel={capitalizePlainString(title)}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

          <PageArticle>
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
                src={
                  "https://forms.zohopublic.com/fluidattacks1/form/Newsletter/formperma/Oj1qU25E49Iy6up1YnEtxsXuOxqbDEl1V5QtvLIAM7c"
                }
                style={{
                  border: "0",
                  height: "500px",
                  width: "99%",
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

export const query: void = graphql`
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
