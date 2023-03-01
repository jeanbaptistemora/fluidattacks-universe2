/*
 *There is no danger using dangerouslySetInnerHTML since everything is built in
 *compile time, also
 *Default exports are needed for pages used in nodes by default to create pages
 *like index.tsx or this one
 */
/* eslint react/no-danger:0 */
/* eslint react/jsx-no-bind:0 */
/* eslint import/no-default-export:0 */
/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-namespace:0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import { graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import React, { useCallback } from "react";

import { Breadcrumbs } from "../components/Breadcrumbs";
import { FloatingButton } from "../components/FloatingButton";
import { InternalCta } from "../components/InternalCta";
import { Seo } from "../components/Seo";
import { ServiceSeo } from "../components/ServiceSeo";
import { Paragraph } from "../components/Texts";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import {
  BigPageContainer,
  BlackH2,
  MarkedTitle,
  PageArticle,
  RedMark,
  ServicesGrid,
  ServicesHeaderContainer,
} from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";

const ContinuousHackingIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const { location } = pageContext.breadcrumb;

  const home = ["/"];
  const path = home.concat(
    location.split("/").filter((name): boolean => name !== "")
  );

  const { description, headtitle, image, keywords, slug, subtext, title } =
    data.markdownRemark.frontmatter;

  const { trackEvent } = useMatomo();

  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({
      action: "float-free-trial-click",
      category: "solution",
    });
  }, [trackEvent]);

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={image}
        keywords={keywords}
        title={
          headtitle
            ? `${headtitle} | Services | Fluid Attacks`
            : `${title} | Services | Fluid Attacks`
        }
        url={slug}
      />
      <ServiceSeo
        description={description}
        image={image.replace(".webp", ".png")}
        title={`${title} | Fluid Attacks`}
        url={`https://fluidattacks.com/${slug}`}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumbs currentPath={path} />

          <PageArticle bgColor={"#f9f9f9"}>
            <BigPageContainer>
              <ServicesHeaderContainer>
                <RedMark>
                  <MarkedTitle>{title}</MarkedTitle>
                </RedMark>
                <Paragraph fColor={"#2e2e38"} fSize={"16"} maxWidth={"1864"}>
                  {subtext}
                </Paragraph>
              </ServicesHeaderContainer>
              <BlackH2>{"Key Features"}</BlackH2>
              <ServicesGrid
                dangerouslySetInnerHTML={{
                  __html: data.markdownRemark.html,
                }}
              />
            </BigPageContainer>
            <InternalCta
              description={translate.t("plansPage.portrait.paragraph")}
              image={"/airs/plans/plans-cta"}
              title={translate.t("plansPage.portrait.title")}
            />
            <FloatingButton
              bgColor={"#2e2e38"}
              color={"#fff"}
              matomoEvent={matomoFreeTrialEvent}
              text={"Start free trial"}
              to={"/free-trial/"}
              yPosition={"50%"}
            />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default ContinuousHackingIndex;

export const query: StaticQueryDocument = graphql`
  query ServiceIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        banner
        description
        keywords
        slug
        subtext
        image
        title
        headtitle
      }
    }
  }
`;
