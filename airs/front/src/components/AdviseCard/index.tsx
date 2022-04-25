/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
import { Link, graphql, useStaticQuery } from "gatsby";
import React from "react";

import {
  AdvisoryCardContainer,
  CardDescription,
  CardDescriptionContainer,
  CardSubtitle,
  CardTitle,
} from "./styles/styledComponents";

import { Badge, PhantomRegularRedButton } from "../../styles/styledComponents";

const AdviseCard: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query AdviseQuery {
      allMarkdownRemark(sort: { fields: [frontmatter___date], order: DESC }) {
        edges {
          node {
            fields {
              slug
            }
            frontmatter {
              advise
              authors
              codename
              cveid
              date
              description
              slug
              title
              severity
            }
          }
        }
      }
    }
  `);

  const adviseInfo = data.allMarkdownRemark.edges.filter(
    (advisePages): boolean => advisePages.node.frontmatter.advise === "yes"
  );

  return (
    <React.StrictMode>
      {adviseInfo.map((advisePage): JSX.Element => {
        const { authors, codename, cveid, date, severity, slug, title } =
          advisePage.node.frontmatter;

        return (
          <AdvisoryCardContainer key={codename}>
            <Badge
              bgColor={"#dddde3"}
              color={"#2e2e38"}
            >{`Severity ${severity}`}</Badge>
            <CardTitle>{title}</CardTitle>
            <CardSubtitle>{cveid}</CardSubtitle>
            <CardDescriptionContainer>
              <CardDescription>{`Published: ${date}`}</CardDescription>
              <CardDescription>{`Discovered by ${authors}`}</CardDescription>
            </CardDescriptionContainer>
            <Link to={`/${slug}`}>
              <PhantomRegularRedButton className={"w-100"}>
                {"Read More"}
              </PhantomRegularRedButton>
            </Link>
          </AdvisoryCardContainer>
        );
      })}
    </React.StrictMode>
  );
};

export { AdviseCard };
