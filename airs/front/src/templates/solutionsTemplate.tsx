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
/* eslint react/jsx-no-bind:0 */
import { graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import React from "react";

import { Breadcrumbs } from "../components/Breadcrumbs";
import { Container } from "../components/Container";
import { Grid } from "../components/Grid";
import { Hero } from "../components/Hero";
import { Seo } from "../components/Seo";
import { VerticalCard } from "../components/VerticalCard";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import { PageArticle } from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";

const SolutionsIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const { location } = pageContext.breadcrumb;

  const home = ["/"];
  const path = home.concat(
    location.split("/").filter((name): boolean => name !== "")
  );

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
          <Breadcrumbs currentPath={path} />
          <PageArticle bgColor={"#ffffff"}>
            <Hero
              button1Link={"/free-trial/"}
              button1Text={"Start free trial"}
              button2Link={"/contact-us/"}
              button2Text={"Contact now"}
              image={"airs/solutions/Index/application-security-solutions"}
              matomoAction={"Solution"}
              paragraph={translate.t("solutions.informations.paragraph")}
              size={"big"}
              sizeSm={"medium"}
              title={translate.t("solutions.informations.subtitle")}
            />
            <Container center={true} maxWidth={"1440px"} ph={4} pv={5}>
              <Grid columns={3} columnsMd={2} columnsSm={1} gap={"1rem"}>
                {solutionData.map((solution): JSX.Element => {
                  return (
                    <VerticalCard
                      alt={solution.title}
                      bgColor={"transparent"}
                      btnDisplay={"inline-block"}
                      btnText={"Explore solution"}
                      btnVariant={"primary"}
                      description={solution.paragraph}
                      image={`airs/solutions/${solution.image}`}
                      imagePadding={true}
                      key={solution.title}
                      link={solution.link}
                      title={solution.title}
                    />
                  );
                })}
              </Grid>
            </Container>
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
