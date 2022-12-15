import { graphql, useStaticQuery } from "gatsby";
import React from "react";

import { Container } from "../../components/Container";
import { Grid } from "../../components/Grid";
import { Pagination } from "../../components/Pagination";
import { Text, Title } from "../../components/Typography";
import { VerticalCard } from "../../components/VerticalCard";
import { usePagination } from "../../utils/hooks";
import { capitalizeDashedString, stringToUri } from "../../utils/utilities";

interface IBlogsAuthorProps {
  authorName: string;
  authorDescription: string | undefined;
  authorTitle: string | undefined;
}

const BlogsAuthorPage: React.FC<IBlogsAuthorProps> = ({
  authorName,
  authorDescription,
  authorTitle,
}): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query NewBlogAuthorList {
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

  const posts: INodes[] = data.allMarkdownRemark.edges.filter(
    (edge): boolean => stringToUri(edge.node.frontmatter.author) === authorName
  );

  const blogsCards = posts.map((post): JSX.Element | undefined => {
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
        key={slug}
        link={slug}
        subMinHeight={"56px"}
        subtitle={subtitle}
        title={title}
        titleMinHeight={"64px"}
      />
    );
  });

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
      <Container mb={3}>
        <Title
          color={"#2e2e38"}
          level={1}
          mb={3}
          size={"big"}
          textAlign={"center"}
        >
          {authorTitle === undefined
            ? capitalizeDashedString(authorName)
            : `Posts by ${authorTitle}`}
        </Title>
        {authorDescription === undefined ? undefined : (
          <Text color={"#2e2e38"} textAlign={"center"}>
            {authorDescription}
          </Text>
        )}
      </Container>
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

export { BlogsAuthorPage };
