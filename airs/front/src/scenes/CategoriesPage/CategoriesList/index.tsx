import { graphql, useStaticQuery } from "gatsby";
import React from "react";

import { AirsLink } from "../../../components/AirsLink";
import { Container } from "../../../components/Container";
import { Grid } from "../../../components/Grid";
import { PresentationCard } from "../../../components/PresentationCard";
import { Title } from "../../../components/Typography";
import { capitalizePlainString } from "../../../utils/utilities";

const CategoriesList: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query NewCategoriesList {
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
              category
            }
          }
        }
      }
    }
  `);

  const categoriesListRaw = data.allMarkdownRemark.edges.map(
    (edge): string => edge.node.frontmatter.category
  );

  const categoriesList = categoriesListRaw.filter(
    (category, index): boolean => categoriesListRaw.indexOf(category) === index
  );

  return (
    <Container ph={4} pv={5}>
      <Title color={"#2e2e38"} level={1} size={"big"} textAlign={"center"}>
        {"Authors:"}
      </Title>
      <Container center={true} maxWidth={"1000px"} pt={5}>
        <Grid columns={3} columnsMd={2} columnsSm={1} gap={"1rem"}>
          {categoriesList.map((category): JSX.Element => {
            return (
              <AirsLink
                decoration={"none"}
                href={`${category}/`}
                key={category}
              >
                <PresentationCard
                  image={`blogs/categories/${category}`}
                  text={capitalizePlainString(category)}
                />
              </AirsLink>
            );
          })}
        </Grid>
      </Container>
    </Container>
  );
};

export { CategoriesList };
