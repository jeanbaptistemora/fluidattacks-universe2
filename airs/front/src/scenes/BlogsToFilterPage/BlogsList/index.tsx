import { graphql, useStaticQuery } from "gatsby";
import React from "react";

import { Container } from "../../../components/Container";
import { Grid } from "../../../components/Grid";
import { Pagination } from "../../../components/Pagination";
import { VerticalCard } from "../../../components/VerticalCard";
import { usePagination } from "../../../utils/hooks";
import { stringToUri } from "../../../utils/utilities";

interface IBlogsListProps {
  filterBy: "author" | "category" | "tag";
  value: string;
}

const BlogsList: React.FC<IBlogsListProps> = ({
  filterBy,
  value,
}): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query BlogsToFilterList {
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
              description
              image
              spanish
              subtitle
              tags
              title
            }
          }
        }
      }
    }
  `);

  const posts: INodes[] = data.allMarkdownRemark.edges;

  const filterAuthors = (post: INodes, author: string): boolean => {
    return stringToUri(post.node.frontmatter.author) === author;
  };

  const filterTags = (post: INodes, tag: string): boolean => {
    return post.node.frontmatter.tags
      .split(", ")
      .some((blogTag): boolean => blogTag === tag);
  };

  const filterCategories = (post: INodes, category: string): boolean => {
    return post.node.frontmatter.category === category;
  };

  const filterBlogs = (
    filter: string,
    filterValue: string,
    blogs: INodes[]
  ): INodes[] => {
    if (filter === "author") {
      return blogs.filter((post): boolean => filterAuthors(post, filterValue));
    } else if (filter === "category") {
      return blogs.filter((post): boolean =>
        filterCategories(post, filterValue)
      );
    }

    return blogs.filter((post): boolean => filterTags(post, filterValue));
  };

  const blogsCards = filterBlogs(filterBy, value, posts).map(
    (post): JSX.Element | undefined => {
      const { slug } = post.node.fields;
      const {
        alt,
        author,
        date,
        description,
        image,
        spanish,
        subtitle,
        title,
      } = post.node.frontmatter;

      return spanish === "yes" ? undefined : (
        <VerticalCard
          alt={alt}
          author={author}
          btnText={"Read post"}
          date={date}
          description={description}
          image={image}
          key={slug}
          link={slug}
          subMinHeight={"56px"}
          subtitle={subtitle}
          title={title}
          titleMinHeight={"64px"}
        />
      );
    }
  );

  const listOfBlogs: (JSX.Element | undefined)[] = blogsCards.filter(
    (post): boolean => {
      return post !== undefined;
    }
  );

  const itemsPerPage = 9;

  const { currentPage, endOffset, handlePageClick, newOffset, pageCount } =
    usePagination(itemsPerPage, listOfBlogs);

  return (
    <Container center={true} maxWidth={"1440px"} ph={4} pv={5}>
      <Grid columns={3} columnsMd={2} columnsSm={1} gap={"1rem"}>
        {listOfBlogs.slice(newOffset, endOffset)}
      </Grid>
      <Pagination
        forcePage={currentPage}
        onChange={handlePageClick}
        pageCount={pageCount}
      />
    </Container>
  );
};

export { BlogsList };
