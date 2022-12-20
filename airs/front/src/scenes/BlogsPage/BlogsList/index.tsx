/* eslint fp/no-mutating-methods:0 */
import dayjs from "dayjs";
import { graphql, useStaticQuery } from "gatsby";
import React, { useCallback, useState } from "react";

import { Button } from "../../../components/Button";
import { Container } from "../../../components/Container";
import { Grid } from "../../../components/Grid";
import { Select, TextArea } from "../../../components/Input";
import { Pagination } from "../../../components/Pagination";
import { Text } from "../../../components/Typography";
import { VerticalCard } from "../../../components/VerticalCard";
import { usePagination } from "../../../utils/hooks";
import { capitalizePlainString } from "../../../utils/utilities";

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

  const categoriesOrder = [
    "interview",
    "politics",
    "development",
    "opinions",
    "philosophy",
    "attacks",
  ];

  const authorsListRaw = data.allMarkdownRemark.edges.map(
    (edge): string => edge.node.frontmatter.author
  );

  const tagsListRaw = data.allMarkdownRemark.edges
    .map((edge): string[] => edge.node.frontmatter.tags.split(", "))
    .flat();

  const categoriesListRaw = data.allMarkdownRemark.edges.map(
    (edge): string => edge.node.frontmatter.category
  );

  const authorsList = authorsListRaw.filter(
    (author, index): boolean => authorsListRaw.indexOf(author) === index
  );

  const tagsList = tagsListRaw.filter(
    (tag, index): boolean => tagsListRaw.indexOf(tag) === index
  );

  const categoriesList = categoriesListRaw.filter(
    (category, index): boolean => categoriesListRaw.indexOf(category) === index
  );

  const sortedCategories = [...categoriesList].sort(
    (first, second): number =>
      categoriesOrder.indexOf(second) - categoriesOrder.indexOf(first)
  );

  const datesList = ["Last month", "Last 6 months", "Last year"];

  const allPosts: INodes[] = data.allMarkdownRemark.edges;

  const [selectedAuthor, setSelectedAuthor] = useState("All");
  const [selectedTag, setSelectedTag] = useState("All");
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedTitle, setSelectedTitle] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");

  const filterAuthors = (post: INodes, author: string): boolean => {
    return author === "All" || post.node.frontmatter.author === author;
  };

  const filterTags = (post: INodes, tag: string): boolean => {
    return (
      tag === "All" ||
      post.node.frontmatter.tags
        .split(", ")
        .some((blogTag): boolean => blogTag === tag)
    );
  };

  const filterDates = (post: INodes, date: string): boolean => {
    if (date === "Last month") {
      return dayjs(post.node.frontmatter.date).isAfter(
        dayjs().subtract(1, "months")
      );
    } else if (date === "Last 6 months") {
      return dayjs(post.node.frontmatter.date).isAfter(
        dayjs().subtract(6, "months")
      );
    } else if (date === "Last year") {
      return dayjs(post.node.frontmatter.date).isAfter(
        dayjs().subtract(1, "year")
      );
    }

    return true;
  };

  const filterTitles = (post: INodes, title: string): boolean => {
    return (
      title === "" ||
      post.node.frontmatter.title.toLowerCase().includes(title.toLowerCase())
    );
  };

  const filterCategories = (post: INodes, category: string): boolean => {
    return category === "All" || post.node.frontmatter.category === category;
  };

  const filterBlogs = (
    author: string,
    tag: string,
    date: string,
    title: string,
    category: string,
    blogs: INodes[]
  ): INodes[] => {
    return blogs
      .filter((post): boolean => filterAuthors(post, author))
      .filter((post): boolean => filterTags(post, tag))
      .filter((post): boolean => filterDates(post, date))
      .filter((post): boolean => filterTitles(post, title))
      .filter((post): boolean => filterCategories(post, category));
  };

  const blogsCards = filterBlogs(
    selectedAuthor,
    selectedTag,
    selectedDate,
    selectedTitle,
    selectedCategory,
    allPosts
  ).map((post): JSX.Element | undefined => {
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

  const {
    currentPage,
    endOffset,
    handlePageClick,
    newOffset,
    pageCount,
    resetPagination,
  } = usePagination(itemsPerPage, listOfBlogs);

  const changeAuthor = useCallback(
    (author: string): void => {
      setSelectedAuthor(author);
      resetPagination();
    },
    [resetPagination]
  );

  const changeTag = useCallback(
    (tag: string): void => {
      setSelectedTag(tag);
      resetPagination();
    },
    [resetPagination]
  );

  const changeDate = useCallback(
    (date: string): void => {
      setSelectedDate(date);
      resetPagination();
    },
    [resetPagination]
  );

  const changeTitle = useCallback(
    (title: string): void => {
      setSelectedTitle(title);
      resetPagination();
    },
    [resetPagination]
  );

  const changeCategory = useCallback(
    (category: string): VoidFunction => {
      return (): void => {
        setSelectedCategory(category);
        resetPagination();
      };
    },
    [resetPagination]
  );

  return (
    <Container bgColor={"#fff"}>
      <Container center={true} maxWidth={"1440px"} ph={4} pv={5}>
        <Grid columns={4} columnsMd={2} columnsSm={1} gap={"1rem"}>
          <Select
            label={"Filter by author:"}
            onChange={changeAuthor}
            options={authorsList}
          />
          <Select
            label={"Filter by tag:"}
            onChange={changeTag}
            options={tagsList}
          />
          <Select
            label={"Release date:"}
            onChange={changeDate}
            options={datesList}
          />
          <TextArea
            label={"Filter by title:"}
            onChange={changeTitle}
            placeHolder={"Search"}
          />
        </Grid>
        <Container display={"flex"} justify={"center"} pv={5} wrap={"wrap"}>
          <Container key={"All"} mh={2} mt={2} width={"auto"}>
            <Button
              onClick={changeCategory("All")}
              selected={selectedCategory === "All"}
            >
              {"View all"}
            </Button>
          </Container>
          {sortedCategories.map((category: string): JSX.Element => {
            return (
              <Container key={category} mh={2} mt={2} width={"auto"}>
                <Button
                  onClick={changeCategory(category)}
                  selected={selectedCategory === category}
                >
                  {capitalizePlainString(category)}
                </Button>
              </Container>
            );
          })}
        </Container>
        {listOfBlogs.length > 0 ? (
          <React.Fragment>
            <Grid columns={3} columnsMd={2} columnsSm={1} gap={"1rem"}>
              {listOfBlogs.slice(newOffset, endOffset)}
            </Grid>
            <Pagination
              forcePage={currentPage}
              onChange={handlePageClick}
              pageCount={pageCount}
            />
          </React.Fragment>
        ) : (
          <Container>
            <Text color={"#2e2e38"} size={"big"} textAlign={"center"}>
              {"There are no blogs to display"}
            </Text>
          </Container>
        )}
      </Container>
    </Container>
  );
};
