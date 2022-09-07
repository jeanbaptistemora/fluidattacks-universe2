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
/* eslint import/no-default-export:0 */
/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-namespace:0 */
import { Link, graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { CloudImage } from "../components/CloudImage";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import { Paragraph, Title } from "../components/Texts";
import {
  FlexCenterItemsContainer,
  PageArticle,
  PageContainer,
  PhantomRegularRedButton,
  SystemsCardContainer,
} from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const SolutionsIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { description, keywords, slug, title } =
    data.markdownRemark.frontmatter;

  const solutionData = [
    {
      image: "solution-devsecops_jgeyje",
      link: "/solutions/devsecops/",
      paragraph: translate.t("solutions.devSecOps.paragraph"),
      title: translate.t("solutions.devSecOps.subtitle"),
    },
    {
      image: "solution-security-testing_mmthfa",
      link: "/solutions/security-testing/",
      paragraph: translate.t("solutions.securityTesting.paragraph"),
      title: translate.t("solutions.securityTesting.subtitle"),
    },
    {
      image: "solution-penetration-testing_ty3kro",
      link: "/solutions/penetration-testing/",
      paragraph: translate.t("solutions.penetrationTesting.paragraph"),
      title: translate.t("solutions.penetrationTesting.subtitle"),
    },
    {
      image: "solution-ethical-hacking_zuhkms",
      link: "/solutions/ethical-hacking/",
      paragraph: translate.t("solutions.ethicalHacking.paragraph"),
      title: translate.t("solutions.ethicalHacking.subtitle"),
    },
    {
      image: "solution-red-teaming_trx6rr",
      link: "/solutions/red-teaming/",
      paragraph: translate.t("solutions.redTeaming.paragraph"),
      title: translate.t("solutions.redTeaming.subtitle"),
    },
    {
      image: "solution-attack-simulation_asqzhr",
      link: "/solutions/attack-simulation/",
      paragraph: translate.t("solutions.attackSimulation.paragraph"),
      title: translate.t("solutions.attackSimulation.subtitle"),
    },
    {
      image: "solution-secure-code-review_dyaluj",
      link: "/solutions/secure-code-review/",
      paragraph: translate.t("solutions.secureCode.paragraph"),
      title: translate.t("solutions.secureCode.subtitle"),
    },
    {
      image: "solution-vulnerability-management_a5xmkt",
      link: "/solutions/vulnerability-management/",
      paragraph: translate.t("solutions.vulnerabilityManagement.paragraph"),
      title: translate.t("solutions.vulnerabilityManagement.subtitle"),
    },
  ];

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

          <PageArticle bgColor={"#f4f4f6"}>
            <FlexCenterItemsContainer>
              <Title fColor={"#2e2e38"} fSize={"48"} marginTop={"4"}>
                {title}
              </Title>
            </FlexCenterItemsContainer>
            <PageContainer className={"flex flex-wrap"}>
              {solutionData.map((solutionCard): JSX.Element => {
                return (
                  <SystemsCardContainer key={solutionCard.title}>
                    <CloudImage
                      alt={title}
                      src={`airs/solutions/${solutionCard.image}`}
                      styles={"w-100"}
                    />
                    <Title
                      fColor={"#2e2e38"}
                      fSize={"24"}
                      marginBottom={"1"}
                      marginTop={"1"}
                    >
                      {solutionCard.title}
                    </Title>
                    <Paragraph
                      fColor={"#5c5c70"}
                      fSize={"16"}
                      marginBottom={"1"}
                    >
                      {solutionCard.paragraph}
                    </Paragraph>
                    <Link to={solutionCard.link}>
                      <PhantomRegularRedButton>
                        {"Go to solution"}
                      </PhantomRegularRedButton>
                    </Link>
                  </SystemsCardContainer>
                );
              })}
            </PageContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default SolutionsIndex;

export const query: StaticQueryDocument = graphql`
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
