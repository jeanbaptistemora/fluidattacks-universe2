/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { faChevronDown } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { graphql, useStaticQuery } from "gatsby";
import React, { useEffect, useState } from "react";
import type { SetStateAction } from "react";

import { BlogCard } from "./BlogCard";
import { BlogMainDiv, LoadMoreButton } from "./StyledComponents";

import { PageArticle } from "../../styles/styledComponents";

interface IData {
  allAsciidoc: {
    edges: [
      {
        node: {
          fields: {
            slug: string;
          };
          document: {
            title: string;
          };
          pageAttributes: {
            alt: string;
            author: string;
            category: string;
            image: string;
            tags: string;
            description: string;
            slug: string;
            subtitle: string;
          };
        };
      }
    ];
  };
}

interface INodes {
  node: {
    fields: {
      slug: string;
    };
    document: {
      title: string;
    };
    pageAttributes: {
      alt: string;
      author: string;
      category: string;
      image: string;
      tags: string;
      description: string;
      slug: string;
      subtitle: string;
    };
  };
}

export const BlogsList: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query BlogsList {
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
            document {
              title
            }
            pageAttributes {
              alt
              author
              category
              slug
              tags
              description
              image
              subtitle
            }
          }
        }
      }
    }
  `);

  const posts: INodes[] = data.allAsciidoc.edges;

  const postsPerPage = 12;
  // eslint-disable-next-line fp/no-let
  let arrayForHoldingPosts: INodes[] = [];

  const [postsToShow, setPostsToShow] = useState([]);
  const [next, setNext] = useState(postsPerPage);

  const loopWithSlice = (start: number, end: number): void => {
    const slicedPosts: INodes[] = posts.slice(start, end);
    // eslint-disable-next-line fp/no-mutation
    arrayForHoldingPosts = [
      ...arrayForHoldingPosts,
      ...slicedPosts,
    ] as INodes[];
    setPostsToShow(arrayForHoldingPosts as SetStateAction<never[]>);
  };

  useEffect((): void => {
    loopWithSlice(0, postsPerPage);
  });

  const handleShowMorePosts = (): void => {
    loopWithSlice(0, next + postsPerPage);
    setNext(next + postsPerPage);
  };

  return (
    <div>
      <PageArticle>
        <BlogMainDiv>
          {(postsToShow as INodes[]).map(
            (post): JSX.Element => (
              <BlogCard
                alt={post.node.pageAttributes.alt}
                author={post.node.pageAttributes.author}
                blogLink={post.node.pageAttributes.slug}
                category={post.node.pageAttributes.category}
                description={post.node.pageAttributes.description}
                image={post.node.pageAttributes.image}
                key={post.node.document.title}
                subtitle={post.node.pageAttributes.subtitle}
                tags={post.node.pageAttributes.tags}
                title={post.node.document.title}
              />
            )
          )}
        </BlogMainDiv>
      </PageArticle>
      {/* eslint-disable-next-line react/jsx-no-bind */}
      <LoadMoreButton onClick={handleShowMorePosts}>
        {"Load more"}
        {/* eslint-disable-next-line react/forbid-component-props */}
        <FontAwesomeIcon className={"f3 db center"} icon={faChevronDown} />
      </LoadMoreButton>
    </div>
  );
};
