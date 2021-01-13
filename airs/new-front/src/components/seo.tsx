import { graphql, StaticQuery } from "gatsby";
import React from "react";
// tslint:disable-next-line: match-default-export-name
import Helmet from "react-helmet";

interface StaticQueryData {
  site: {
    siteMetadata: {
      description: string;
      keywords: [string];
      title: string;
    };
  };
}

interface Props {
  readonly description?: string;
  readonly keywords?: string[];
  readonly lang?: string;
  readonly title: string;
}

export const SEO: React.FC<Props> = ({ title, description, lang, keywords }: Props): JSX.Element => (
<StaticQuery
    // tslint:disable-next-line: no-void-expression
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
      const metaDescription: string = description as string;
      const language: string = lang as string;
      const kwords: string[] = keywords as string[];

      return (
        <Helmet
          htmlAttributes={{
            language,
          }}
          title={title}
          titleTemplate={`%s | ${data.site.siteMetadata.title}`}
          meta={[
            {
              content: metaDescription,
              name: "description",
            },
            {
              content: title,
              property: "og:title",
            },
            {
              content: metaDescription,
              property: "og:description",
            },
            {
              content: "website",
              property: "og:type",
            },
          ].concat(
            kwords.length > 0
              ? {
                  content: kwords.join(", "),
                  name: "keywords",
                }
              : [],
          )}
        />
      );
    }}
  />
);
