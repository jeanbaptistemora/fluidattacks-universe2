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

  const posts: INodes[] = data.allAsciidoc.edges.filter((edge): boolean =>
    edge.node.pageAttributes.tags.includes(tagName)
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
