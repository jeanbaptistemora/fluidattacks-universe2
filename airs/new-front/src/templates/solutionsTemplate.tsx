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
import * as devSecOpsImage from "../assets/images/solutions/solution-1.png";
import {
  ArticleContainer,
  BannerContainer,
  BannerTitle,
  BlackListItemSpaced,
  FullWidthContainer,
  HalfScreenContainer,
  HalfScreenContainerSpaced,
  PageArticle,
  PageContainer,
  SolutionsParagraph,
  SolutionsSectionDescription,
  SolutionsSubtitle,
} from "../styles/styledComponents";
import { Link, graphql } from "gatsby";
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
        title={title}
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
                <FullWidthContainer className={"pv3 flex-l"}>
                  <HalfScreenContainer className={"fl-l tl"}>
                    <img alt={"devSecOps Solution"} src={devSecOpsImage} />
                  </HalfScreenContainer>
                  <HalfScreenContainerSpaced className={"fr-l"}>
                    <SolutionsSectionDescription>
                      <BlackListItemSpaced>
                        <Link
                          className={
                            "c-fluid-bk underlined-animated no-underline mt0 mb3 t-all-5"
                          }
                          to={"."}>
                          <SolutionsSubtitle>{"DevSecOps"}</SolutionsSubtitle>
                        </Link>
                        <SolutionsParagraph>
                          {
                            "You can integrate security into your DevOps approach at any time in \
                             your SDLC and ensure your team’s accountability."
                          }
                        </SolutionsParagraph>
                      </BlackListItemSpaced>
                    </SolutionsSectionDescription>
                  </HalfScreenContainerSpaced>
                </FullWidthContainer>
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
  query PageArticle($slug: String!) {
    asciidoc(fields: { slug: { eq: $slug } }) {
      document {
        title
      }
      html
      fields {
        slug
      }
      pageAttributes {
        description
        keywords
        slug
        banner
      }
    }
  }
`;
