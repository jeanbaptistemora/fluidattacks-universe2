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

const CategoriesList: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query CategoriesList {
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

  const categoriesSet = new Set(categoriesListRaw);

  return (
    <React.Fragment>
      <BlogItemTitle>{"Categories:"}</BlogItemTitle>
      <BlogItemListContainer>
        <BlogItemList>
          {Array.from(categoriesSet).map(
            (category): JSX.Element => (
              <BlogItemItem key={category}>
                <Link to={`/blog/categories/${category}`}>
                  <BlogItemName>
                    {`${decode(category)} (${countCoincidences(
                      category,
                      categoriesListRaw
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

export { CategoriesList };
