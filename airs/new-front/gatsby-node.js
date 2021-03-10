const _ = require(`lodash`);
const path = require(`path`);
const { createFilePath } = require(`gatsby-source-filesystem`);

const pagetemplate = path.resolve(`./src/templates/solutionsTemplate.tsx`);
const defaultTemplate = path.resolve(`./src/templates/pageArticle.tsx`);

const setTemplate = (template) => (result = `${template}Template.tsx`);

/**
 * @param {*func} createPage
 */
const PageMaker = (createPage) => {
  return {
    createTemplatePage(posts) {
      _.each(posts, (post) => {
        if (post.node.pageAttributes.template == null) {
          createPage({
            path: post.node.pageAttributes.slug,
            component: defaultTemplate,
            context: {
              id: post.node.id,
              slug: `/${post.node.pageAttributes.slug}`,
            },
          });
        } else {
          createPage({
            path: post.node.pageAttributes.slug,
            component: pagetemplate,
            context: {
              id: post.node.id,
              slug: `/${post.node.pageAttributes.slug}`,
            },
          });
        }
      });
    },
  };
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
        allAsciidoc(limit: 2000) {
          edges {
            node {
              id
              pageAttributes {
                slug
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

    const posts = result.data.allAsciidoc.edges;

    pageMaker.createTemplatePage(posts);
  });
};

exports.onCreateNode = async ({ node, actions, getNode, loadNodeContent }) => {
  const { createNodeField } = actions;

  if (node.internal.type === `Asciidoc`) {
    const value = createFilePath({ node, getNode });
    createNodeField({
      name: `slug`,
      node,
      value,
    });
  }
};
