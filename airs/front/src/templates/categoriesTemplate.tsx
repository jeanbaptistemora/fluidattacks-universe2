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
import { Seo } from "../components/Seo";
import { Paragraph, Title } from "../components/Texts";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import {
  FlexCenterItemsContainer,
  PageArticle,
  PageContainer,
  PhantomRegularRedButton,
  SystemsCardContainer,
} from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const CategoriesIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { description, keywords, slug, title } =
    data.markdownRemark.frontmatter;

  const categoryData = [
    {
      image: "sast",
      link: "/product/sast/",
      paragraph: translate.t("categories.sast.paragraph"),
      title: translate.t("categories.sast.subtitle"),
    },
    {
      image: "dast",
      link: "/product/dast/",
      paragraph: translate.t("categories.dast.paragraph"),
      title: translate.t("categories.dast.subtitle"),
    },
    {
      image: "mpt",
      link: "/solutions/penetration-testing/",
      paragraph: translate.t("categories.mpt.paragraph"),
      title: translate.t("categories.mpt.subtitle"),
    },
    {
      image: "sca",
      link: "/product/sca/",
      paragraph: translate.t("categories.sca.paragraph"),
      title: translate.t("categories.sca.subtitle"),
    },
    {
      image: "re",
      link: "/product/re/",
      paragraph: translate.t("categories.re.paragraph"),
      title: translate.t("categories.re.subtitle"),
    },
    {
      image: "ptaas",
      link: "/product/ptaas/",
      paragraph: translate.t("categories.ptaas.paragraph"),
      title: translate.t("categories.ptaas.subtitle"),
    },
    {
      image: "mast",
      link: "/product/mast/",
      paragraph: translate.t("categories.mast.paragraph"),
      title: translate.t("categories.mast.subtitle"),
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
              {categoryData.map((categoryCard): JSX.Element => {
                return (
                  <SystemsCardContainer key={categoryCard.title}>
                    <CloudImage
                      alt={title}
                      src={`airs/product/${categoryCard.image}-card`}
                      styles={"w-100"}
                    />
                    <Title
                      fColor={"#2e2e38"}
                      fSize={"24"}
                      marginBottom={"1"}
                      marginTop={"1"}
                    >
                      {categoryCard.title}
                    </Title>
                    <Paragraph
                      fColor={"#5c5c70"}
                      fSize={"16"}
                      marginBottom={"1"}
                    >
                      {categoryCard.paragraph}
                    </Paragraph>
                    <Link to={categoryCard.link}>
                      <PhantomRegularRedButton>
                        {"Go to product"}
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

export default CategoriesIndex;

export const query: StaticQueryDocument = graphql`
  query CategoriesIndex($slug: String!) {
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
