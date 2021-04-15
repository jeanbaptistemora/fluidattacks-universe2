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
/* eslint import/no-namespace:0 */
import { graphql } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import devSecOpsImage from "../../static/images/solutions/solution-1.png"; // eslint-disable-line import/no-unresolved
import securityTestingImage from "../../static/images/solutions/solution-2.png"; // eslint-disable-line import/no-unresolved
import penetrationTestingImage from "../../static/images/solutions/solution-3.png"; // eslint-disable-line import/no-unresolved
import ethicalHackingImage from "../../static/images/solutions/solution-4.png"; // eslint-disable-line import/no-unresolved
import redTeamingImage from "../../static/images/solutions/solution-5.png"; // eslint-disable-line import/no-unresolved
import attackSimulationImage from "../../static/images/solutions/solution-6.png"; // eslint-disable-line import/no-unresolved
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import { SolutionsIndexContent } from "../components/SolutionsIndexContent";
import {
  ArticleContainer,
  BannerContainer,
  BannerTitle,
  FullWidthContainer,
  PageArticle,
  PageContainer,
} from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";

const SolutionsIndex: React.FC<IQueryData> = ({
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
            <BannerContainer className={banner}>
              <FullWidthContainer>
                <BannerTitle>{title}</BannerTitle>
              </FullWidthContainer>
            </BannerContainer>
            <ArticleContainer>
              <PageContainer>
                <SolutionsIndexContent
                  animation={"animate__slideInLeft"}
                  image={devSecOpsImage}
                  imageAllignment={"fl-l tl"}
                  link={"/solutions/devsecops/"}
                  paragraph={translate.t("solutions.devSecOps.paragraph")}
                  paragraphAllignment={"fr-l"}
                  subtitle={translate.t("solutions.devSecOps.subtitle")}
                />

                <SolutionsIndexContent
                  animation={"animate__slideInLeft"}
                  image={securityTestingImage}
                  imageAllignment={"fl-l tl"}
                  link={"/solutions/security-testing/"}
                  paragraph={translate.t("solutions.securityTesting.paragraph")}
                  paragraphAllignment={"fr-l"}
                  subtitle={translate.t("solutions.securityTesting.subtitle")}
                />

                <SolutionsIndexContent
                  animation={"animate__slideInLeft"}
                  image={penetrationTestingImage}
                  imageAllignment={"fl-l tl"}
                  link={"/solutions/penetration-testing/"}
                  padding={"pb6"}
                  paragraph={translate.t(
                    "solutions.penetrationTesting.paragraph"
                  )}
                  paragraphAllignment={"fr-l"}
                  subtitle={translate.t(
                    "solutions.penetrationTesting.subtitle"
                  )}
                />

                <SolutionsIndexContent
                  animation={"animate__slideInRight"}
                  image={ethicalHackingImage}
                  imageAllignment={"fr-l tl"}
                  link={"/solutions/ethical-hacking/"}
                  paragraph={translate.t("solutions.ethicalHacking.paragraph")}
                  paragraphAllignment={"fl-l"}
                  subtitle={translate.t("solutions.ethicalHacking.subtitle")}
                />

                <SolutionsIndexContent
                  animation={"animate__slideInRight"}
                  image={redTeamingImage}
                  imageAllignment={"fr-l tl"}
                  link={"/solutions/red-teaming/"}
                  paragraph={translate.t("solutions.redTeaming.paragraph")}
                  paragraphAllignment={"fl-l"}
                  subtitle={translate.t("solutions.redTeaming.subtitle")}
                />

                <SolutionsIndexContent
                  animation={"animate__slideInRight"}
                  image={attackSimulationImage}
                  imageAllignment={"fr-l tl"}
                  link={"/solutions/attack-simulation/"}
                  paragraph={translate.t(
                    "solutions.attackSimulation.paragraph"
                  )}
                  paragraphAllignment={"fl-l"}
                  subtitle={translate.t("solutions.attackSimulation.subtitle")}
                />
              </PageContainer>
            </ArticleContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default SolutionsIndex;

export const query: void = graphql`
  query SolutionsIndex($slug: String!) {
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
        description
        keywords
        slug
      }
    }
  }
`;
