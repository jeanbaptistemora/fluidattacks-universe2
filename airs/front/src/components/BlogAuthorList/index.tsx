/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint require-unicode-regexp:0 */
import { graphql, useStaticQuery } from "gatsby";
import React, { useEffect, useState } from "react";
import type { SetStateAction } from "react";
import { RiArrowDownSFill } from "react-icons/ri";

import { stringToUri } from "../../utils/utilities";
import { BlogCard } from "../BlogsList/BlogCard";
import { BlogMainDiv, LoadMoreButton } from "../BlogsList/StyledComponents";

const BlogAuthorList: React.FC<{ authorName: string }> = ({
  authorName,
}: {
  authorName: string;
}): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query BlogAuthorList {
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
              alt
              author
              category
              date
              slug
              tags
              description
              image
              spanish
              subtitle
              title
            }
          }
        }
      }
    }
  `);

  const posts: INodes[] = data.allMarkdownRemark.edges.filter(
    (edge): boolean => stringToUri(edge.node.frontmatter.author) === authorName
  );

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
    <React.Fragment>
      <BlogMainDiv>
        {(postsToShow as INodes[]).map((post): JSX.Element | undefined => {
          const {
            alt,
            date,
            description,
            image,
            slug,
            spanish,
            subtitle,
            title,
          } = post.node.frontmatter;

          return spanish === "yes" ? undefined : (
            <BlogCard
              alt={alt}
              blogLink={slug}
              date={date}
              description={description}
              image={image}
              key={title}
              subtitle={subtitle}
              title={title}
            />
          );
        })}
      </BlogMainDiv>
      {/* eslint-disable-next-line react/jsx-no-bind */}
      <LoadMoreButton onClick={handleShowMorePosts}>
        {"Load more"}
        {/* eslint-disable-next-line react/forbid-component-props */}
        <RiArrowDownSFill className={"f3 db center"} />
      </LoadMoreButton>
    </React.Fragment>
  );
};

export { BlogAuthorList };
