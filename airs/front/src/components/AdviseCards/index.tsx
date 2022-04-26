/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
import { Link, graphql, useStaticQuery } from "gatsby";
import React, { useCallback, useState } from "react";

import {
  AdvisoriesGrid,
  AdvisoryCardContainer,
  CardDescription,
  CardDescriptionContainer,
  CardSubtitle,
  CardTitle,
} from "./styles/styledComponents";

import { Badge, PhantomRegularRedButton } from "../../styles/styledComponents";
import { Pagination } from "../Pagination";

const AdviseCards: React.FC = (): JSX.Element => {
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

  const listOfCards = adviseInfo.map((advisePage): JSX.Element => {
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
  });

  const itemsPerPage = 6;
  const pageCount = Math.ceil(listOfCards.length / itemsPerPage);
  const [currentItems, setCurrentItems] = useState(
    listOfCards.slice(0, itemsPerPage)
  );

  const handlePageClick = useCallback(
    (prop: { selected: number }): void => {
      const { selected } = prop;
      const newOffset = (selected * itemsPerPage) % listOfCards.length;
      const endOffset = newOffset + itemsPerPage;
      setCurrentItems(listOfCards.slice(newOffset, endOffset));
    },
    [listOfCards]
  );

  return (
    <React.Fragment>
      <AdvisoriesGrid>{currentItems}</AdvisoriesGrid>
      <Pagination onChange={handlePageClick} pageCount={pageCount} />
    </React.Fragment>
  );
};

export { AdviseCards };
