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
import { capitalizeObject } from "../utils/utilities";

const SubscribeIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { title } = data.asciidoc.document;
  const customCrumbLabel: string = `${title
    .charAt(0)
    .toUpperCase()}${title.slice(1).replace("-", "")}`;

  return (
    <React.Fragment>
      <Seo
        description={data.asciidoc.pageAttributes.description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619631770/airs/contact-us/bg-contact-us_cpcyoj.png"
        }
        keywords={data.asciidoc.pageAttributes.keywords}
        title={`${title} | Fluid Attacks`}
        url={data.asciidoc.pageAttributes.slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={customCrumbLabel}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

          <PageArticle>
            <PageHeader
              banner={"contact-bg"}
              pageWithBanner={true}
              slug={data.asciidoc.pageAttributes.slug}
              subtext={data.asciidoc.pageAttributes.subtext}
              subtitle={data.asciidoc.pageAttributes.subtitle}
              title={title}
            />

            <IframeContainer>
              <iframe
                height={"350px"}
                src={
                  "https://crm.zoho.com/crm/WebFormServeServlet?rid=78c3d7dacbbcd07154bafdf9da4878771bc21b44c283c816928cd4453788f1c6gid1a8b1be45eb673e71a5b1925197e4664b5207c89778ad1e7315be647827aaa2d"
                }
                title={"Subscribe Form"}
                width={"610px"}
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
    asciidoc(fields: { slug: { eq: $slug } }) {
      document {
        title
      }
      fields {
        slug
      }
      pageAttributes {
        description
        keywords
      }
    }
  }
`;
