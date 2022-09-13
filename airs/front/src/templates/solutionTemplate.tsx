/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { FloatingButton } from "../components/FloatingButton";
import { InternalCta } from "../components/InternalCta";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import { ServiceSeo } from "../components/ServiceSeo";
import { Paragraph } from "../components/Texts";
import {
  BlackH2,
  ComplianceContainer,
  FlexCenterItemsContainer,
  FullWidthContainer,
  MarkedTitle,
  PageArticle,
  RedMark,
} from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const SolutionIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { description, image, keywords, slug, solution, title } =
    data.markdownRemark.frontmatter;

  const { trackEvent } = useMatomo();

  const matomoFreeTrialEvent = (): void => {
    trackEvent({
      action: "float-free-trial-click",
      category: "solution",
    });
  };

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619630822/airs/solutions/bg-solutions_ylz99o.png"
        }
        keywords={keywords}
        title={`${title} | Fluid Attacks`}
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
          <Breadcrumb
            crumbLabel={capitalizePlainString(title)}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

          <PageArticle bgColor={"#f4f4f6"}>
            <ComplianceContainer>
              <RedMark>
                <MarkedTitle>{title}</MarkedTitle>
              </RedMark>
              <Paragraph fColor={"#2e2e38"} fSize={"16"} marginTop={"1"}>
                {solution}
              </Paragraph>
              <FullWidthContainer>
                <BlackH2>{translate.t("solution.benefits")}</BlackH2>
                <FlexCenterItemsContainer
                  className={"solution-benefits flex-wrap"}
                  dangerouslySetInnerHTML={{
                    __html: data.markdownRemark.html,
                  }}
                />
              </FullWidthContainer>
            </ComplianceContainer>
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

export default SolutionIndex;

export const query: StaticQueryDocument = graphql`
  query SolutionIndex($slug: String!) {
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
        solution
        image
        title
      }
    }
  }
`;
