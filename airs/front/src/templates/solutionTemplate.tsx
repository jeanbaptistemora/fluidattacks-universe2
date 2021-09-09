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

import { CloudImage } from "../components/CloudImage";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import { ShadowedCard } from "../components/ShadowedCard";
import {
  BigPageContainer,
  BigSolutionParagraph,
  BlackH2,
  BlackSolutionParagraph,
  CardsContainer,
  CenteredSpacedContainer,
  FlexCenterItemsContainer,
  FullWidthContainer,
  MarkedTitle,
  PageArticle,
  PageContainer,
  RedMark,
  RegularRedButton,
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

  const {
    description,
    image,
    keywords,
    slug,
    solution,
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
            <BigPageContainer>
              <CloudImage
                alt={"Solution Image"}
                src={`/airs/solutions/solution-${image}`}
                styles={"ml-solution"}
              />
              <RedMark className={"ml-solution"}>
                <MarkedTitle>{title}</MarkedTitle>
              </RedMark>
              <FullWidthContainer className={"pv4"}>
                <div className={"tl  ml-solution"}>
                  <BigSolutionParagraph className={"tl"}>
                    {solution}
                  </BigSolutionParagraph>
                </div>
              </FullWidthContainer>
              <FullWidthContainer>
                <BlackH2>{translate.t("solution.benefits")}</BlackH2>
                <FlexCenterItemsContainer
                  className={"solution-benefits flex-wrap"}
                  dangerouslySetInnerHTML={{
                    __html: data.markdownRemark.html,
                  }}
                />
              </FullWidthContainer>
            </BigPageContainer>
            <PageContainer>
              <FullWidthContainer className={"pv4"}>
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
                  <ShadowedCard
                    color={"bg-black-18"}
                    image={"/airs/solutions/icon-skull"}
                    number={translate.t("solution.cards.vulnerabilities")}
                    text={translate.t("solution.cards.vulnerabilitiesText")}
                  />
                  <ShadowedCard
                    color={"bg-black-18"}
                    image={"/airs/solutions/icon-lock"}
                    number={translate.t("solution.cards.percentage")}
                    text={translate.t("solution.cards.percentageText")}
                  />
                  <ShadowedCard
                    color={"bg-black-18"}
                    image={"/airs/solutions/icon-security"}
                    number={translate.t("solution.cards.hackers")}
                    text={translate.t("solution.cards.hackersText")}
                  />
                  <ShadowedCard
                    color={"bg-black-18"}
                    image={"/airs/solutions/icon-fly"}
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
