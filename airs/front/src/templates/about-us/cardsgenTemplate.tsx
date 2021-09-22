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
import { graphql } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { CertificationsPage } from "../../components/CertificationsPage";
import { ClientsPage } from "../../components/ClientsPage";
import { Layout } from "../../components/Layout";
import { NavbarComponent } from "../../components/Navbar";
import { PartnerPage } from "../../components/PartnerPage";
import { Seo } from "../../components/Seo";
import {
  BannerContainer,
  BannerTitle,
  CardsContainer1200,
  FullWidthContainer,
  PageArticle,
} from "../../styles/styledComponents";
import { capitalizeObject, capitalizePlainString } from "../../utils/utilities";

const CardsgenIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const {
    banner,
    clientsindex,
    certificationsindex,
    description,
    keywords,
    partnersindex,
    slug,
    title,
  } = data.markdownRemark.frontmatter;

  const metaImage: string =
    partnersindex === "yes"
      ? "https://res.cloudinary.com/fluid-attacks/image/upload/v1619633627/airs/partners/cover-partners_n4sshp.png"
      : clientsindex === "yes"
      ? "https://res.cloudinary.com/fluid-attacks/image/upload/v1619635918/airs/about-us/clients/cover-clients_llnlaw.png"
      : "https://res.cloudinary.com/fluid-attacks/image/upload/v1619632703/airs/about-us/certifications/cover-certifications_dos6xu.png";

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={metaImage}
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
            <BannerContainer className={banner}>
              <FullWidthContainer>
                <BannerTitle>{title}</BannerTitle>
              </FullWidthContainer>
            </BannerContainer>
            <CardsContainer1200>
              <div
                dangerouslySetInnerHTML={{
                  __html: data.markdownRemark.html,
                }}
              />
              {partnersindex === "yes" ? (
                <PartnerPage />
              ) : clientsindex === "yes" ? (
                <ClientsPage />
              ) : certificationsindex === "yes" ? (
                <CertificationsPage />
              ) : undefined}
            </CardsContainer1200>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default CardsgenIndex;

export const query: void = graphql`
  query CardsgenPages($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        banner
        certificationsindex
        clientsindex
        description
        keywords
        slug
        partnersindex
        title
      }
    }
  }
`;
