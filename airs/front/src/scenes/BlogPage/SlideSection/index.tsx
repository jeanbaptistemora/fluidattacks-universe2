/* eslint fp/no-mutating-methods:0 */
import { graphql, useStaticQuery } from "gatsby";
import React from "react";

import { CardSlideShow } from "../../../components/CardSlideShow";

interface ISlideSectionProps {
  slug: string;
  tags: string;
}

const SlideSection: React.FC<ISlideSectionProps> = ({
  slug,
  tags,
}): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query RecommendedBlogsList {
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
              subtitle
            }
          }
        }
      }
    }
  `);

  const blogs: INodes[] = data.allMarkdownRemark.edges;

  const tagsList = tags.split(", ").flat();

  const filterBlogs: INodes[] = blogs.filter((post): boolean => {
    return tagsList.some((tag): boolean => {
      return (
        post.node.frontmatter.tags.includes(tag) &&
        post.node.frontmatter.slug !== slug
      );
    });
  });

  const blogsList = filterBlogs.slice(0, 8);

  return (
    <CardSlideShow
      btnText={"Read post"}
      containerDescription={"Recommended blog posts"}
      containerTitle={"You might be interested in the following related posts."}
      data={blogsList}
    />
  );
};

export { SlideSection };
