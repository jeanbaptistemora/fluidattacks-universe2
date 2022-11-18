/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint fp/no-mutating-methods:0 */
import { graphql, useStaticQuery } from "gatsby";
import React, { useEffect, useState } from "react";

import { CardSlideShow } from "../../../../components/CardSlideShow";

interface ISolutionSlideShowProps {
  description: string;
  tag: string;
  title: string;
}

const SolutionSlideShow: React.FC<ISolutionSlideShowProps> = ({
  description,
  tag,
  title,
}): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query SolutionBlogList {
      allMarkdownRemark(
        filter: {
          fields: { slug: { regex: "/blog/" } }
          frontmatter: { image: { regex: "" }, spanish: { eq: null } }
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
              slug
              tags
              description
              image
              title
            }
          }
        }
      }
    }
  `);

  const sortList = {
    devsevops: [
      "/blog/aws-devsecops-with-fluid-attacks/",
      "/blog/why-is-cloud-devsecops-important/",
      "/blog/what-does-a-devsecops-engineer-do/",
      "/blog/devsecops-best-practices/",
      "/blog/devsecops-tools/",
      "/blog/how-to-implement-devsecops/",
      "/blog/devsecops-concept/",
    ],
  };

  const blogs: INodes[] = data.allMarkdownRemark.edges.filter((edge): boolean =>
    edge.node.frontmatter.tags.includes(tag)
  );

  const [sortedBlogs, setSortedBlogs] = useState<INodes[]>(blogs);

  useEffect((): void => {
    function sortBlogs(toSort: string[]): void {
      const sortingBlogs = [...sortedBlogs];
      sortingBlogs.sort(
        (first, second): number =>
          toSort.indexOf(second.node.fields.slug) -
          toSort.indexOf(first.node.fields.slug)
      );
      setSortedBlogs(sortingBlogs);
    }

    if (tag === "devsecops") {
      sortBlogs(sortList.devsevops);
    }
  });

  return (
    <CardSlideShow
      btnText={"Read post"}
      containerDescription={description}
      containerTitle={title}
      data={sortedBlogs}
    />
  );
};

export { SolutionSlideShow };
