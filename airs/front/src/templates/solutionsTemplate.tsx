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

import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import { SolutionsIndexContent } from "../components/SolutionsIndexContent";
import {
  MarkedTitle,
  MarkedTitleContainer,
  PageArticle,
  PageContainer,
  RedMark,
} from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const redTeamingImage: string =
  "https://res.cloudinary.com/fluid-attacks/image/upload/v1619735155/airs/solutions/solution-red-teaming_trx6rr.webp";
const devSecOpsImage: string =
  "https://res.cloudinary.com/fluid-attacks/image/upload/v1619735154/airs/solutions/solution-devsecops_jgeyje.webp";
const ethicalHackingImage: string =
  "https://res.cloudinary.com/fluid-attacks/image/upload/v1619735154/airs/solutions/solution-ethical-hacking_zuhkms.webp";
const attackSimulationImage: string =
  "https://res.cloudinary.com/fluid-attacks/image/upload/v1619735154/airs/solutions/solution-attack-simulation_asqzhr.webp";
const penetrationTestingImage: string =
  "https://res.cloudinary.com/fluid-attacks/image/upload/v1619735154/airs/solutions/solution-penetration-testing_ty3kro.webp";
const securityTestingImage: string =
  "https://res.cloudinary.com/fluid-attacks/image/upload/v1619735154/airs/solutions/solution-security-testing_mmthfa.webp";
const secureCodeReviewImage: string =
  "https://res.cloudinary.com/fluid-attacks/image/upload/v1622577351/airs/solutions/solution-secure-code-review_dyaluj.webp";
const vulnerabilityManagementImage: string =
  "https://res.cloudinary.com/fluid-attacks/image/upload/v1622578216/airs/solutions/solution-vulnerability-management_a5xmkt.webp";

const SolutionsIndex: React.FC<IQueryData> = ({
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
    title,
  } = data.markdownRemark.frontmatter;

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

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={capitalizePlainString(title)}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

          <PageArticle>
            <MarkedTitleContainer>
              <div className={"ph-body"}>
                <RedMark>
                  <MarkedTitle>{title}</MarkedTitle>
                </RedMark>
              </div>
              <PageContainer className={"flex flex-wrap"}>
                <SolutionsIndexContent
                  animation={"animate__slideInLeft"}
                  image={devSecOpsImage}
                  link={"/solutions/devsecops/"}
                  paragraph={translate.t("solutions.devSecOps.paragraph")}
                  subtitle={translate.t("solutions.devSecOps.subtitle")}
                />

                <SolutionsIndexContent
                  animation={"animate__slideInRight"}
                  image={securityTestingImage}
                  link={"/solutions/security-testing/"}
                  paragraph={translate.t("solutions.securityTesting.paragraph")}
                  subtitle={translate.t("solutions.securityTesting.subtitle")}
                />

                <SolutionsIndexContent
                  animation={"animate__slideInLeft"}
                  image={penetrationTestingImage}
                  link={"/solutions/penetration-testing/"}
                  paragraph={translate.t(
                    "solutions.penetrationTesting.paragraph"
                  )}
                  subtitle={translate.t(
                    "solutions.penetrationTesting.subtitle"
                  )}
                />

                <SolutionsIndexContent
                  animation={"animate__slideInRight"}
                  image={ethicalHackingImage}
                  link={"/solutions/ethical-hacking/"}
                  paragraph={translate.t("solutions.ethicalHacking.paragraph")}
                  subtitle={translate.t("solutions.ethicalHacking.subtitle")}
                />

                <SolutionsIndexContent
                  animation={"animate__slideInLeft"}
                  image={redTeamingImage}
                  link={"/solutions/red-teaming/"}
                  paragraph={translate.t("solutions.redTeaming.paragraph")}
                  subtitle={translate.t("solutions.redTeaming.subtitle")}
                />

                <SolutionsIndexContent
                  animation={"animate__slideInRight"}
                  image={attackSimulationImage}
                  link={"/solutions/attack-simulation/"}
                  paragraph={translate.t(
                    "solutions.attackSimulation.paragraph"
                  )}
                  subtitle={translate.t("solutions.attackSimulation.subtitle")}
                />

                <SolutionsIndexContent
                  animation={"animate__slideInLeft"}
                  image={secureCodeReviewImage}
                  link={"/solutions/secure-code-review/"}
                  paragraph={translate.t("solutions.secureCode.paragraph")}
                  subtitle={translate.t("solutions.secureCode.subtitle")}
                />

                <SolutionsIndexContent
                  animation={"animate__slideInRight"}
                  image={vulnerabilityManagementImage}
                  link={"/solutions/vulnerability-management/"}
                  paragraph={translate.t(
                    "solutions.vulnerabilityManagement.paragraph"
                  )}
                  subtitle={translate.t(
                    "solutions.vulnerabilityManagement.subtitle"
                  )}
                />
              </PageContainer>
            </MarkedTitleContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default SolutionsIndex;

export const query: void = graphql`
  query SolutionsIndex($slug: String!) {
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
        title
      }
    }
  }
`;
