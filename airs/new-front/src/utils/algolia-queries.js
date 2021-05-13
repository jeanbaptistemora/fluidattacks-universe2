const pageQuery = `{
  pages: allAsciidoc(
    filter: {fields: {slug: {regex: ""}}}
  ) {
    edges {
      node {
        id
        document {
          title
        }
        fields {
          slug
        }
        pageAttributes {
          description
        }
      }
    }
  }
}`

function pageToAlgoliaRecord({ node: { id, document, fields, pageAttributes, ...rest } }) {
  return {
    objectID: id,
    ...document,
    ...id,
    ...fields,
    ...pageAttributes,
    ...rest,
  }
}

const settings = { attributesToSnippet: [`excerpt:20`] }

const queries = [
  {
    query: pageQuery,
    transformer: ({ data }) => data.pages.edges.map(pageToAlgoliaRecord),
    indexName: `fluidattacks_airs`,
    settings,
  },
]

module.exports = queries
