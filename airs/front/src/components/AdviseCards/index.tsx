/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
import { graphql, useStaticQuery } from "gatsby";
import React from "react";

import { CardFooter } from "./styles/styledComponents";

import { Badge } from "../../styles/styledComponents";
import { usePagination } from "../../utils/hooks";
import { AirsLink } from "../AirsLink";
import { Button } from "../Button";
import { Container } from "../Container";
import { Grid } from "../Grid";
import { Pagination } from "../Pagination";
import { Text } from "../Typography";

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
              encrypted
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

  const listOfCards = adviseInfo.map((advisePage): JSX.Element | undefined => {
    const { authors, codename, cveid, date, encrypted, severity, slug, title } =
      advisePage.node.frontmatter;

    return encrypted === "yes" ? undefined : (
      <Container
        bgColor={"#fff"}
        br={3}
        direction={"column"}
        display={"flex"}
        key={codename}
        mh={2}
        mv={2}
        ph={3}
        pv={3}
      >
        <Container pv={2}>
          <Badge
            bgColor={"#dddde3"}
            color={"#2e2e38"}
          >{`Severity ${severity}`}</Badge>
        </Container>
        <Container minHeight={"56px"} mt={3}>
          <Text color={"#2e2e38"} size={"big"} weight={"bold"}>
            {title}
          </Text>
        </Container>
        <Container mv={3}>
          <Text color={"#787891"} size={"big"} weight={"bold"}>
            {cveid}
          </Text>
        </Container>
        <CardFooter>
          <Text color={"#787891"} size={"medium"}>{`Published: ${date}`}</Text>
          <Text
            color={"#787891"}
            mb={3}
            size={"medium"}
          >{`Discovered by ${authors}`}</Text>
          <AirsLink href={`/${slug}`}>
            <Button display={"block"} variant={"tertiary"}>
              {"Read More"}
            </Button>
          </AirsLink>
        </CardFooter>
      </Container>
    );
  });

  const cleanListOfCards: (JSX.Element | undefined)[] = listOfCards.filter(
    (card): boolean => {
      return card !== undefined;
    }
  );

  const itemsPerPage = 9;

  const { currentPage, endOffset, handlePageClick, newOffset, pageCount } =
    usePagination(itemsPerPage, cleanListOfCards);

  return (
    <React.Fragment>
      <Container center={true} maxWidth={"1300px"} ph={4} pv={5}>
        <Grid columns={3} columnsMd={2} columnsSm={1} gap={"1rem"}>
          {cleanListOfCards.slice(newOffset, endOffset)}
        </Grid>
      </Container>
      <Pagination
        forcePage={currentPage}
        onChange={handlePageClick}
        pageCount={pageCount}
      />
    </React.Fragment>
  );
};

export { AdviseCards };
