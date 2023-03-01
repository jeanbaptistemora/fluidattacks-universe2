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
import { Link, graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import React from "react";

import { AdviseCards } from "../components/AdviseCards";
import { Breadcrumbs } from "../components/Breadcrumbs";
import { Seo } from "../components/Seo";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import {
  AdvisoriesContainer,
  BannerContainer,
  BannerSubtitle,
  BannerTitle,
  FullWidthContainer,
  NewRegularRedButton,
  PageArticle,
} from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";

const AdvisoriesIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const { location } = pageContext.breadcrumb;

  const home = ["/"];
  const path = home.concat(
    location.split("/").filter((name): boolean => name !== "")
  );

  const { banner, description, keywords, slug, subtitle, title } =
    data.markdownRemark.frontmatter;

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

          <PageArticle bgColor={"#dddde3"}>
            <BannerContainer className={banner}>
              <FullWidthContainer>
                <BannerTitle>{title}</BannerTitle>
                <BannerSubtitle>{subtitle}</BannerSubtitle>
              </FullWidthContainer>
            </BannerContainer>
            <AdviseCards />
            <AdvisoriesContainer>
              <h4 className={"f3 c-fluid-bk poppins"}>{`${translate.t(
                "advisories.disclosurePhrase"
              )} `}</h4>
              <Link to={"/advisories/policy"}>
                <NewRegularRedButton
                  className={"w-auto-ns w-100"}
                >{`${translate.t(
                  "advisories.buttonPhrase"
                )} `}</NewRegularRedButton>
              </Link>
            </AdvisoriesContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default AdvisoriesIndex;

export const query: StaticQueryDocument = graphql`
  query AdvisoriesIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        description
        banner
        keywords
        slug
        title
        subtitle
      }
    }
  }
`;
