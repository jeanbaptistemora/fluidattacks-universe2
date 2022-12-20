import { graphql, useStaticQuery } from "gatsby";
import React from "react";

import { AirsLink } from "../../../components/AirsLink";
import { Container } from "../../../components/Container";
import { Grid } from "../../../components/Grid";
import { PresentationCard } from "../../../components/PresentationCard";
import { capitalizeDashedString } from "../../../utils/utilities";

const TagsList: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query NewTagsList {
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
              tags
            }
          }
        }
      }
    }
  `);

  const tagsListRaw = data.allMarkdownRemark.edges
    .map((edge): string[] => edge.node.frontmatter.tags.split(", "))
    .flat();

  const tagsList = tagsListRaw.filter(
    (tag, index): boolean => tagsListRaw.indexOf(tag) === index
  );

  return (
    <Container ph={4} pv={5}>
      <Container center={true} maxWidth={"1000px"}>
        <Grid columns={3} columnsMd={2} columnsSm={1} gap={"1rem"}>
          {tagsList.map((tag): JSX.Element => {
            return (
              <AirsLink decoration={"none"} href={`${tag}/`} key={tag}>
                <PresentationCard
                  image={`blogs/tags/default`}
                  text={capitalizeDashedString(tag)}
                />
              </AirsLink>
            );
          })}
        </Grid>
      </Container>
    </Container>
  );
};

export { TagsList };
