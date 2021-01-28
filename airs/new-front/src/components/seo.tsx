/*
 *These rules are disabled since the usage are for performance issues,
 *but this will be a static site, so everything in this file is going to
 *be ran at compile time
 */
/* eslint @typescript-eslint/no-non-null-assertion: 0 */
/* eslint react/jsx-no-bind: 0 */
/* eslint react/default-props-match-prop-types:0 */
import Helmet from "react-helmet";

import React from "react";

import { StaticQuery, graphql } from "gatsby";

interface IStaticQueryData {
  site: {
    siteMetadata: {
      description: string;
      keywords: [string];
      title: string;
    };
  };
}

interface IProps {
  description?: string;
  keywords?: string[];
  lang?: string;
  title: string;
}

const defaultProps: IProps = {
  description: "",
  keywords: [""],
  lang: "en_US",
  title: "",
};

const SEO: React.FC<IProps> = ({
  title,
  description,
  lang,
  keywords,
}: IProps): JSX.Element => (
  <StaticQuery
    // eslint-disable-next-line @typescript-eslint/no-confusing-void-expression
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
    render={(data: IStaticQueryData): React.ReactElement | null => {
      const metaDescription: string = description!;
      const language: string = lang!;
      const kwords: string[] = keywords!;

      return (
        <Helmet
          htmlAttributes={{
            language,
          }}
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
              : []
          )}
          title={title}
          titleTemplate={`%s | ${data.site.siteMetadata.title}`}
        />
      );
    }}
  />
);

// eslint-disable-next-line fp/no-mutation
SEO.defaultProps = defaultProps;

export { SEO };
