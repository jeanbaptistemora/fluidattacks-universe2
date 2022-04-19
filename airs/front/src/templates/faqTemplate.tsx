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
/* eslint fp/no-mutation: 0 */
/* eslint react/forbid-component-props: 0 */
/* eslint react/jsx-no-bind:0 */
import { graphql } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import { decode } from "he";
import React, { useEffect, useState } from "react";
import type { SetStateAction } from "react";

import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { PageHeader } from "../components/PageHeader";
import { Seo } from "../components/Seo";
import {
  CenteredSpacedContainer,
  FaqContainer,
  FaqPageArticle,
  PhantomRegularRedButton,
} from "../styles/styledComponents";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const FaqIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { banner, description, keywords, slug, subtext, subtitle, title } =
    data.markdownRemark.frontmatter;

  const hasBanner: boolean = typeof banner === "string";

  const questions = data.markdownRemark.html.split("</div>");
  const questionsPerPage = 10;

  // eslint-disable-next-line fp/no-let
  let arrayForHoldingQuestions: string[] = [];

  const [questionsToShow, setQuestionsToShow] = useState([]);
  const [next, setNext] = useState(questionsPerPage);

  const loopWithSlice = (start: number, end: number): void => {
    const slicedPosts = questions.slice(start, end);
    // eslint-disable-next-line fp/no-mutation
    arrayForHoldingQuestions = [...arrayForHoldingQuestions, ...slicedPosts];
    setQuestionsToShow(arrayForHoldingQuestions as SetStateAction<never[]>);
  };

  useEffect((): void => {
    loopWithSlice(0, questionsPerPage);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleShowMorePosts = (): void => {
    loopWithSlice(0, next + questionsPerPage);
    setNext(next + questionsPerPage);
  };

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/c_scale,w_1200/v1622583388/airs/logo_fluid_attacks_2021_eqop3k.png"
        }
        keywords={keywords}
        title={decode(`${title} | Fluid Attacks`)}
        url={slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={decode(capitalizePlainString(title))}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

          <FaqPageArticle>
            <PageHeader
              banner={banner}
              pageWithBanner={hasBanner}
              slug={slug}
              subtext={subtext}
              subtitle={subtitle}
              title={decode(title)}
            />
            <FaqContainer>
              {questionsToShow.map((question): JSX.Element => {
                return (
                  <div
                    dangerouslySetInnerHTML={{
                      __html: question,
                    }}
                    key={question}
                  />
                );
              })}

              <CenteredSpacedContainer>
                <PhantomRegularRedButton
                  className={"w-50-ns w-100"}
                  onClick={handleShowMorePosts}
                >
                  {"Show more"}
                </PhantomRegularRedButton>
              </CenteredSpacedContainer>
            </FaqContainer>
          </FaqPageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default FaqIndex;

export const query: void = graphql`
  query FaqIndex($slug: String!) {
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
