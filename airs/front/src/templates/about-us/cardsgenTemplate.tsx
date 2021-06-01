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
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { CertificationsPage } from "../../components/CertificationsPage";
import { ClientsPage } from "../../components/ClientsPage";
import { Layout } from "../../components/Layout";
import { NavbarComponent } from "../../components/Navbar";
import { PartnerPage } from "../../components/PartnerPage";
import { Seo } from "../../components/Seo";
import {
  BannerContainer,
  BannerTitle,
  FullWidthContainer,
  PageArticle,
} from "../../styles/styledComponents";
import { capitalizeCrumbs } from "../../utils/capitalizeCrumbs";

const CardsgenIndex: React.FC<IQueryData> = ({
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

  const { banner } = data.asciidoc.pageAttributes;
  const CardsContainer: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
      roboto
      internal
      mw-1200
      center
      roboto
      bg-lightgray
      ph4-l
      ph3
      pt5-l
      pt4
      pb5
    `,
  })``;
  const metaImage: string =
    data.asciidoc.pageAttributes.partnersindex === "yes"
      ? "https://res.cloudinary.com/fluid-attacks/image/upload/v1619633627/airs/partners/cover-partners_n4sshp.webp"
      : data.asciidoc.pageAttributes.clientsindex === "yes"
      ? "https://res.cloudinary.com/fluid-attacks/image/upload/v1619635918/airs/about-us/clients/cover-clients_llnlaw.webp"
      : "https://res.cloudinary.com/fluid-attacks/image/upload/v1619632703/airs/about-us/certifications/cover-certifications_dos6xu.webp";

  return (
    <React.Fragment>
      <Seo
        description={data.asciidoc.pageAttributes.description}
        image={metaImage}
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
            crumbs={capitalizeCrumbs(crumbs)}
          />

          <PageArticle>
            <BannerContainer className={banner}>
              <FullWidthContainer>
                <BannerTitle>{title}</BannerTitle>
              </FullWidthContainer>
            </BannerContainer>
            <CardsContainer>
              <div
                dangerouslySetInnerHTML={{
                  __html: data.asciidoc.html,
                }}
              />
              {data.asciidoc.pageAttributes.partnersindex === "yes" ? (
                <PartnerPage />
              ) : data.asciidoc.pageAttributes.clientsindex === "yes" ? (
                <ClientsPage />
              ) : data.asciidoc.pageAttributes.certificationsindex === "yes" ? (
                <CertificationsPage />
              ) : undefined}
            </CardsContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default CardsgenIndex;

export const query: void = graphql`
  query CardsgenPages($slug: String!) {
    asciidoc(fields: { slug: { eq: $slug } }) {
      document {
        title
      }
      html
      fields {
        slug
      }
      pageAttributes {
        banner
        certificationsindex
        clientsindex
        description
        keywords
        slug
        partnersindex
      }
    }
  }
`;
