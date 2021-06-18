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

const CategoriesList: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query CategoriesList {
      allAsciidoc(
        filter: {
          fields: { slug: { regex: "/blog/" } }
          pageAttributes: { image: { regex: "" } }
        }
        sort: { fields: pageAttributes___date, order: DESC }
      ) {
        edges {
          node {
            fields {
              slug
            }
            pageAttributes {
              category
            }
          }
        }
      }
    }
  `);

  const categoriesListRaw = data.allAsciidoc.edges.map(
    (edge): string => edge.node.pageAttributes.category
  );

  const countCoincidences: (category: string) => number = (
    category: string
  ): number => {
    const categoriesCount: number = categoriesListRaw.filter(
      (item): boolean => item === category
    ).length;

    return categoriesCount;
  };

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
                    {`${decode(category)} (${countCoincidences(category)})`}
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
