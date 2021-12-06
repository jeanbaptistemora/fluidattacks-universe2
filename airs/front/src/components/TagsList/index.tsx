/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { Link, graphql, useStaticQuery } from "gatsby";
import { decode } from "he";
import React from "react";

import {
  BlogItemItem,
  BlogItemList,
  BlogItemListContainer,
  BlogItemName,
  BlogItemTitle,
} from "../../styles/styledComponents";
import { countCoincidences } from "../../utils/utilities";

const TagsList: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query TagsList {
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

  const tagsSet = new Set(tagsListRaw);

  return (
    <React.Fragment>
      <BlogItemTitle>{"Tags:"}</BlogItemTitle>
      <BlogItemListContainer>
        <BlogItemList>
          {Array.from(tagsSet).map(
            (tag): JSX.Element => (
              <BlogItemItem key={tag}>
                <Link to={`/blog/tags/${tag}`}>
                  <BlogItemName>
                    {`${decode(tag)} (${countCoincidences(tag, tagsListRaw)})`}
                  </BlogItemName>
                </Link>
              </BlogItemItem>
            )
          )}
        </BlogItemList>
      </BlogItemListContainer>
    </React.Fragment>
  );
};

export { TagsList };
