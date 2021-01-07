import React from "react";
import Helmet from "react-helmet";
import {StaticQuery, graphql} from "gatsby";

type StaticQueryData = {
  site: {
    siteMetadata: {
      title: string
      description: string
      keywords: [String]
    }
  }
}

interface IProps {
  readonly title: string
  readonly description?: string
  readonly lang?: string
  readonly keywords?: string[]
}

const SEO: React.FC<IProps> = ({ title, description, lang, keywords }) => (
<StaticQuery
    query={graphql`
      query {
        site {
          siteMetadata {
            title
            description
          }
        }
      }
    `}
    render={(data: StaticQueryData): React.ReactElement | null => {
      const metaDescription = description || data.site.siteMetadata.description
      lang = lang || "es"
      keywords = keywords || []
      return (
        <Helmet
          htmlAttributes={{
            lang,
          }}
          title={title}
          titleTemplate={`%s | ${data.site.siteMetadata.title}`}
          meta={[
            {
              name: `description`,
              content: metaDescription,
            },
            {
              property: `og:title`,
              content: title,
            },
            {
              property: `og:description`,
              content: metaDescription,
            },
            {
              property: `og:type`,
              content: `website`,
            },
          ].concat(
            keywords.length > 0
              ? {
                  name: `keywords`,
                  content: keywords.join(`, `),
                }
              : [],
          )}
        />
      )
    }}
  />
)

export default SEO
