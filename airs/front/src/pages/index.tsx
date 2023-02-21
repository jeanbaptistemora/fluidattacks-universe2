/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import React from "react";

import { Seo } from "../components/Seo";
import { Layout } from "../scenes/Footer/Layout";
import { HomePage } from "../scenes/HomePage";
import { NavbarComponent } from "../scenes/Menu";

const NewHomeIndex: React.FC<IQueryData> = ({
  data,
}: IQueryData): JSX.Element => {
  const { author, description, keywords, siteUrl, title } =
    data.site.siteMetadata;

  return (
    <React.Fragment>
      <Seo
        author={author}
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1669230787/airs/logo-fluid-2022.png"
        }
        keywords={keywords}
        title={title}
        url={siteUrl}
      />

      <Layout>
        <div>
          <NavbarComponent />

          <HomePage />
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default NewHomeIndex;

export const query: StaticQueryDocument = graphql`
  query {
    site {
      siteMetadata {
        author
        description
        keywords
        siteUrl
        title
      }
    }
  }
`;
