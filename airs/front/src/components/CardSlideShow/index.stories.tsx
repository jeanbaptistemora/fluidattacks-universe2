/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import { graphql, useStaticQuery } from "gatsby";
import React from "react";

import type { ICardSlideShowProps } from "./types";

import { CardSlideShow } from ".";

const config: Meta = {
  component: CardSlideShow,
  title: "components/CardSlideShow",
};

const Template: Story<
  React.PropsWithChildren<ICardSlideShowProps>
> = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query StoryBlogList {
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

  const posts: INodes[] = data.allMarkdownRemark.edges.filter((edge): boolean =>
    edge.node.frontmatter.tags.includes("devsecops")
  );

  return (
    <CardSlideShow
      btnText={"Read post"}
      containerDescription={"Read posts about DevSecOps"}
      containerTitle={"Devsecops"}
      data={posts}
    />
  );
};

const Default = Template.bind({});

export { Default };
export default config;
