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
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import { Layout } from "../components/layout";
import { NavbarComponent } from "../components/navbar";
import React from "react";
import { Seo } from "../components/seo";
import { SolutionsIndexContent } from "../components/solutions/solutionsIndexContent";
import { graphql } from "gatsby";
import { translate } from "../utils/translations/translate";
import * as attackSimulationImage from "../assets/images/solutions/solution-6.png";
import * as devSecOpsImage from "../assets/images/solutions/solution-1.png";
import * as ethicalHackingImage from "../assets/images/solutions/solution-4.png";
import * as penetrationTestingImage from "../assets/images/solutions/solution-3.png";
import * as redTeamingImage from "../assets/images/solutions/solution-5.png";
import * as securityTestingImage from "../assets/images/solutions/solution-2.png";
import {
  ArticleContainer,
  BannerContainer,
  BannerTitle,
  FullWidthContainer,
  PageArticle,
  PageContainer,
} from "../styles/styledComponents";
import "../assets/scss/index.scss";

interface IQueryData {
  data: {
    asciidoc: {
      document: {
        title: string;
      };
      html: string;
      fields: {
        slug: string;
      };
      pageAttributes: {
        banner?: string;
        description: string;
        keywords: string;
        slug: string;
      };
    };
  };
  pageContext: {
    breadcrumb: {
      location: string;
      crumbs: [
        {
          pathname: string;
          crumbLabel: string;
        }
      ];
    };
    slug: string;
  };
}

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

  const banner: string = data.asciidoc.pageAttributes.banner as string;

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
                  image={devSecOpsImage}
                  imageAllignment={"fl-l tl"}
                  paragraph={translate.t("solutions.devSecOps.paragraph")}
                  paragraphAllignment={"fr-l"}
                  subtitle={translate.t("solutions.devSecOps.subtitle")}
                />

                <SolutionsIndexContent
                  image={securityTestingImage}
                  imageAllignment={"fl-l tl"}
                  paragraph={translate.t("solutions.securityTesting.paragraph")}
                  paragraphAllignment={"fr-l"}
                  subtitle={translate.t("solutions.securityTesting.subtitle")}
                />

                <SolutionsIndexContent
                  image={penetrationTestingImage}
                  imageAllignment={"fl-l tl"}
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
                  image={ethicalHackingImage}
                  imageAllignment={"fr-l tl"}
                  paragraph={translate.t("solutions.ethicalHacking.paragraph")}
                  paragraphAllignment={"fl-l"}
                  subtitle={translate.t("solutions.ethicalHacking.subtitle")}
                />

                <SolutionsIndexContent
                  image={redTeamingImage}
                  imageAllignment={"fr-l tl"}
                  paragraph={translate.t("solutions.redTeaming.paragraph")}
                  paragraphAllignment={"fl-l"}
                  subtitle={translate.t("solutions.redTeaming.subtitle")}
                />

                <SolutionsIndexContent
                  image={attackSimulationImage}
                  imageAllignment={"fr-l tl"}
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
