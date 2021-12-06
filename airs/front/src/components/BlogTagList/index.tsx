/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint require-unicode-regexp:0 */
import { faChevronDown } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { graphql, useStaticQuery } from "gatsby";
import React, { useEffect, useState } from "react";
import type { SetStateAction } from "react";

import { BlogCard } from "../BlogsList/BlogCard";
import { BlogMainDiv, LoadMoreButton } from "../BlogsList/StyledComponents";

const BlogTagList: React.FC<{ tagName: string }> = ({
  tagName,
}: {
  tagName: string;
}): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query BlogTagList {
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

  const posts: INodes[] = data.allMarkdownRemark.edges.filter((edge): boolean =>
    edge.node.frontmatter.tags.includes(tagName)
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
        {(postsToShow as INodes[]).map((post): JSX.Element | unknown => {
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
        <FontAwesomeIcon className={"f3 db center"} icon={faChevronDown} />
      </LoadMoreButton>
    </React.Fragment>
  );
};

export { BlogTagList };
