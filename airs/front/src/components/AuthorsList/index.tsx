/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint require-unicode-regexp:0 */
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
import { countCoincidences, stringToUri } from "../../utils/utilities";

const AuthorsList: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query AuthorsList {
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
            }
          }
        }
      }
    }
  `);

  const authorsListRaw = data.allMarkdownRemark.edges.map(
    (edge): string => edge.node.frontmatter.author
  );

  const authorsSet = new Set(authorsListRaw);

  return (
    <React.Fragment>
      <BlogItemTitle>{"Authors:"}</BlogItemTitle>
      <BlogItemListContainer>
        <BlogItemList>
          {Array.from(authorsSet).map(
            (author): JSX.Element => (
              <BlogItemItem key={author}>
                <Link to={`/blog/authors/${stringToUri(author)}`}>
                  <BlogItemName>
                    {`${decode(author)} (${countCoincidences(
                      author,
                      authorsListRaw
                    )})`}
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

export { AuthorsList };
