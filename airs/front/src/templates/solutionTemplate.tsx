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
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import { WhiteShadowedCard } from "../components/WhiteShadowedCard";
import {
  BannerContainer,
  BannerTitle,
  BlackH2,
  BlackSolutionParagraph,
  CardsContainer,
  CenteredSpacedContainer,
  FlexCenterItemsContainer,
  FullWidthContainer,
  PageArticle,
  PageContainer,
  RegularRedButton,
} from "../styles/styledComponents";
import { capitalizeCrumbs } from "../utils/capitalizeCrumbs";
import { translate } from "../utils/translations/translate";

const SolutionIndex: React.FC<IQueryData> = ({
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
            crumbs={capitalizeCrumbs(crumbs)}
          />

          <PageArticle>
            <BannerContainer className={"bg-solutions"}>
              <FullWidthContainer>
                <BannerTitle>{title}</BannerTitle>
              </FullWidthContainer>
            </BannerContainer>
            <PageContainer>
              <FullWidthContainer className={"pv4"}>
                <FlexCenterItemsContainer className={"flex-wrap center"}>
                  <div>
                    <div className={"tl"}>
                      <BlackSolutionParagraph className={"tl"}>
                        {data.asciidoc.pageAttributes.solution}
                      </BlackSolutionParagraph>
                    </div>
                  </div>
                </FlexCenterItemsContainer>
              </FullWidthContainer>
              <FullWidthContainer className={"pv4"}>
                <BlackH2>{translate.t("solution.benefits")}</BlackH2>
                <FlexCenterItemsContainer
                  className={"solution-benefits flex-wrap"}
                  dangerouslySetInnerHTML={{
                    __html: data.asciidoc.html,
                  }}
                />
                <CenteredSpacedContainer>
                  <BlackSolutionParagraph className={"tc"}>
                    {`${title} ${translate.t("solution.belonging")} `}
                    <Link
                      className={"basic-link"}
                      to={"/services/continuous-hacking/"}
                    >
                      {"Continuous Hacking"}
                    </Link>
                    {" service"}
                  </BlackSolutionParagraph>
                </CenteredSpacedContainer>
                <CenteredSpacedContainer>
                  <Link to={"/contact-us/"}>
                    <RegularRedButton>
                      {translate.t("contactUs.contactFluidAttacks")}
                    </RegularRedButton>
                  </Link>
                </CenteredSpacedContainer>
              </FullWidthContainer>
              <FullWidthContainer className={"pv4"}>
                <BlackH2>{translate.t("solution.cardsTitle")}</BlackH2>
                <CardsContainer>
                  <WhiteShadowedCard
                    number={translate.t("solution.cards.vulnerabilities")}
                    text={translate.t("solution.cards.vulnerabilitiesText")}
                  />
                  <WhiteShadowedCard
                    number={translate.t("solution.cards.percentage")}
                    text={translate.t("solution.cards.percentageText")}
                  />
                  <WhiteShadowedCard
                    number={translate.t("solution.cards.hackers")}
                    text={translate.t("solution.cards.hackersText")}
                  />
                  <WhiteShadowedCard
                    number={translate.t("solution.cards.owasp")}
                    text={translate.t("solution.cards.owaspText")}
                  />
                </CardsContainer>
              </FullWidthContainer>
            </PageContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default SolutionIndex;

export const query: void = graphql`
  query SolutionIndex($slug: String!) {
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
        solution
      }
    }
  }
`;
