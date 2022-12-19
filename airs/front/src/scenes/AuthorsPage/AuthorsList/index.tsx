import { graphql, useStaticQuery } from "gatsby";
import React from "react";

import { AirsLink } from "../../../components/AirsLink";
import { Container } from "../../../components/Container";
import { Grid } from "../../../components/Grid";
import { PresentationCard } from "../../../components/PresentationCard";
import { stringToUri } from "../../../utils/utilities";

interface IAuthor {
  name: string;
  nickName: string;
}

const AuthorsList: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query NewAuthorsList {
      allMarkdownRemark(
        filter: {
          fields: { slug: { regex: "/blog/" } }
          frontmatter: { image: { regex: "" } }
        }
        sort: { fields: frontmatter___date, order: DESC }
      ) {
        edges {
          node {
            fields {
              slug
            }
            frontmatter {
              author
              writer
            }
          }
        }
      }
    }
  `);

  const authorsListRaw = data.allMarkdownRemark.edges.map((edge): IAuthor => {
    return {
      name: edge.node.frontmatter.author,
      nickName: edge.node.frontmatter.writer,
    };
  });

  const authorsData = authorsListRaw.filter(
    (authorData, index): boolean =>
      authorsListRaw.findIndex(
        (author): boolean =>
          author.name === authorData.name &&
          author.nickName === authorData.nickName
      ) === index
  );

  return (
    <Container ph={4} pv={5}>
      <Container center={true} maxWidth={"1000px"} pt={5}>
        <Grid columns={3} columnsMd={2} columnsSm={1} gap={"1rem"}>
          {authorsData.map((authorData): JSX.Element => {
            const { name, nickName } = authorData;

            return (
              <AirsLink
                decoration={"none"}
                href={`${stringToUri(name)}/`}
                key={name}
              >
                <PresentationCard image={`authors/${nickName}`} text={name} />
              </AirsLink>
            );
          })}
        </Grid>
      </Container>
    </Container>
  );
};

export { AuthorsList };
