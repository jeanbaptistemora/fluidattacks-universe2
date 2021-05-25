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

const ContacUsIndex: React.FC<IQueryData> = ({
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
            crumbs={crumbs}
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
                height={"500px"}
                src={
                  "https://crm.zoho.com/crm/WebFormServeServlet?rid=78c3d7dacbbcd07154bafdf9da4878771131756c5fc0387baa3f5706a0968b4bgid1a8b1be45eb673e71a5b1925197e4664b5207c89778ad1e7315be647827aaa2d"
                }
                title={"Contact Us Form"}
                width={"610px"}
              />
            </IframeContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default ContacUsIndex;

export const query: void = graphql`
  query ContactUsIndex($slug: String!) {
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
