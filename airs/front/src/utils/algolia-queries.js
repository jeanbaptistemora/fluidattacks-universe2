const pageQuery = `{
  pages: allMarkdownRemark(
    filter: {fields: {slug: {regex: ""}}}
  ) {
    edges {
      node {
        id
        fields {
          slug
        }
        frontmatter {
          author
          description
          keywords
          title
        }
      }
    }
  }
}`;

function pageToAlgoliaRecord({
  node: { id, fields, frontmatter, ...rest },
}) {
  return {
    objectID: id,
    ...fields,
    ...frontmatter,
    ...rest,
  };
}

const settings = { attributesToSnippet: [`excerpt:20`] };

const queries = [
  {
    query: pageQuery,
    transformer: ({ data }) => data.pages.edges.map(pageToAlgoliaRecord),
    indexName: `fluidattacks_airs`,
    settings,
  },
];

module.exports = queries;
