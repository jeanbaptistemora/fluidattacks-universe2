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

const ContacUsIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { title } = data.asciidoc.document;
  const {
    description,
    keywords,
    slug,
    subtext,
    subtitle,
  } = data.asciidoc.pageAttributes;

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
