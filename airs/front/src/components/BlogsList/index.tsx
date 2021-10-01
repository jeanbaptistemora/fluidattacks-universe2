/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { faChevronDown } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { graphql, useStaticQuery } from "gatsby";
import React, { useEffect, useState } from "react";
import type { SetStateAction } from "react";

import { BlogCard } from "./BlogCard";
import { BlogMainDiv, LoadMoreButton } from "./StyledComponents";

import { BlogPageArticle } from "../../styles/styledComponents";

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
              date
              slug
              description
              image
              spanish
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
    arrayForHoldingPosts = [...arrayForHoldingPosts, ...slicedPosts];
    setPostsToShow(arrayForHoldingPosts as SetStateAction<never[]>);
  };

  useEffect((): void => {
    loopWithSlice(0, postsPerPage);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleShowMorePosts = (): void => {
    loopWithSlice(0, next + postsPerPage);
    setNext(next + postsPerPage);
  };

  return (
    <div>
      <BlogPageArticle>
        <BlogMainDiv>
          {(postsToShow as INodes[]).map((post): JSX.Element | unknown => {
            const {
              alt,
              date,
              description,
              image,
              slug,
              spanish,
              subtitle,
            } = post.node.pageAttributes;

            return spanish === "yes" ? undefined : (
              <BlogCard
                alt={alt}
                blogLink={slug}
                date={date}
                description={description}
                image={image}
                key={post.node.document.title}
                subtitle={subtitle}
                title={post.node.document.title}
              />
            );
          })}
        </BlogMainDiv>
        {/* eslint-disable-next-line react/jsx-no-bind */}
        <LoadMoreButton onClick={handleShowMorePosts}>
          {"Load more"}
          {/* eslint-disable-next-line react/forbid-component-props */}
          <FontAwesomeIcon className={"f3 db center"} icon={faChevronDown} />
        </LoadMoreButton>
      </BlogPageArticle>
    </div>
  );
};
