import { graphql, useStaticQuery } from "gatsby";
import React from "react";

import { Container } from "../../../components/Container";
import { Grid } from "../../../components/Grid";
import { Pagination } from "../../../components/Pagination";
import { VerticalCard } from "../../../components/VerticalCard";
import { usePagination } from "../../../utils/hooks";

export const BlogsList: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query NewBlogsList {
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
              date
              slug
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

  const posts: INodes[] = data.allMarkdownRemark.edges;

  const listOfBlogs = posts.map((post): JSX.Element | undefined => {
    const { slug } = post.node.fields;
    const { alt, author, date, description, image, spanish, subtitle, title } =
      post.node.frontmatter;

    return spanish === "yes" ? undefined : (
      <VerticalCard
        alt={alt}
        author={author}
        btnText={"Read post"}
        date={date}
        description={description}
        image={image}
        link={slug}
        subMinHeight={"56px"}
        subtitle={subtitle}
        title={title}
        titleMinHeight={"64px"}
      />
    );
  });

  const cleanListOfBlogs: (JSX.Element | undefined)[] = listOfBlogs.filter(
    (post): boolean => {
      return post !== undefined;
    }
  );

  const itemsPerPage = 9;

  const { currentItems, handlePageClick, pageCount } = usePagination(
    itemsPerPage,
    cleanListOfBlogs
  );

  return (
    <Container bgColor={"#fff"}>
      <Container center={true} maxWidth={"1440px"} ph={4} pv={5}>
        <Grid columns={3} columnsMd={2} columnsSm={1} gap={"1rem"}>
          {currentItems}
        </Grid>
        <Pagination onChange={handlePageClick} pageCount={pageCount} />
      </Container>
    </Container>
  );
};
