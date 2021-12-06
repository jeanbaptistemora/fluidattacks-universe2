const _ = require(`lodash`);
const path = require(`path`);
const { createFilePath } = require(`gatsby-source-filesystem`);

const defaultTemplate = path.resolve(`./src/templates/pageArticle.tsx`);
const blogsTemplate = path.resolve(`./src/templates/blogsTemplate.tsx`);

const setTemplate = (template) =>
  path.resolve(`./src/templates/${template}Template.tsx`);

/**
 * @param {*func} createPage
 */
const PageMaker = (createPage) => {
  return {
    createTemplatePage(posts) {
      _.each(posts, (post) => {
        if (post.node.fields.slug.startsWith("/pages/")) {
          if (post.node.frontmatter.template == null) {
            createPage({
              path: `${post.node.frontmatter.slug}`,
              component: defaultTemplate,
              context: {
                id: post.node.id,
                slug: `/pages/${post.node.frontmatter.slug}`,
              },
            });
          } else {
            createPage({
              path: `${post.node.frontmatter.slug}`,
              component: setTemplate(post.node.frontmatter.template),
              context: {
                id: post.node.id,
                slug: `/pages/${post.node.frontmatter.slug}`,
              },
            });
          }
        } else if (post.node.fields.slug.startsWith("/blog/")) {
          createPage({
            path: `/blog/${post.node.frontmatter.slug}`,
            component: blogsTemplate,
            context: {
              id: post.node.id,
              slug: `/blog/${post.node.frontmatter.slug}`,
            },
          });
        }
      });
    },
  };
};

const createTagPages = (createPage, posts) => {
  const tagTemplate = path.resolve(`./src/templates/blogTagTemplate.tsx`);
  const tags = [];

  posts.map((post) => {
    if (
      post.node.fields.slug.startsWith("/blog/") &&
      post.node.frontmatter.tags
    ) {
      tags.push(post.node.frontmatter.tags.split(", "));
    }
  });

  const tagsList = tags.flat();

  tagsList.forEach((tagName) => {
    createPage({
      path: `blog/tags/${tagName}`,
      component: tagTemplate,
      context: { tagName },
    });
  });
};

const createCategoryPages = (createPage, posts) => {
  const categoryTemplate = path.resolve(
    `./src/templates/blogCategoryTemplate.tsx`
  );
  const categories = [];

  posts.map((post) => {
    if (
      post.node.fields.slug.startsWith("/blog/") &&
      post.node.frontmatter.category
    ) {
      categories.push(post.node.frontmatter.category.toLowerCase());
    }
  });

  const categoriesList = categories.flat();

  categoriesList.forEach((categoryName) => {
    createPage({
      path: `blog/categories/${categoryName}`,
      component: categoryTemplate,
      context: { categoryName },
    });
  });
};

const createAuthorPages = (createPage, posts) => {
  const authorTemplate = path.resolve(`./src/templates/blogAuthorTemplate.tsx`);
  const authors = [];

  posts.map((post) => {
    if (
      post.node.fields.slug.startsWith("/blog/") &&
      post.node.frontmatter.author
    ) {
      authors.push(
        post.node.frontmatter.author
          .toLowerCase()
          .replace(" ", "-")
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "")
      );
    }
  });

  const authorsList = authors.flat();

  authorsList.forEach((authorName) => {
    createPage({
      path: `blog/authors/${authorName}`,
      component: authorTemplate,
      context: { authorName },
    });
  });
};

exports.createPages = ({ graphql, actions: { createPage } }) => {
  const pageMaker = PageMaker(createPage);
  // The “graphql” function allows us to run arbitrary
  // queries against the local Drupal graphql schema. Think of
  // it like the site has a built-in database constructed
  // from the fetched data that you can run queries against.
  return graphql(
    `
      {
        allMarkdownRemark(limit: 2000) {
          edges {
            node {
              id
              fields {
                slug
              }
              frontmatter {
                slug
                tags
                category
                author
                writer
                template
              }
            }
          }
        }
      }
    `
  ).then((result) => {
    if (result.errors) {
      throw result.errors;
    }

    const posts = result.data.allMarkdownRemark.edges;

    pageMaker.createTemplatePage(posts);
    createTagPages(createPage, posts);
    createAuthorPages(createPage, posts);
    createCategoryPages(createPage, posts);
  });
};

exports.onCreateNode = async ({ node, actions, getNode, loadNodeContent }) => {
  const { createNodeField } = actions;

  if (node.internal.type === `Asciidoc` || node.internal.type === `MarkdownRemark`) {
    const value = createFilePath({ node, getNode });
    createNodeField({
      name: `slug`,
      node,
      value,
    });
  }
};
