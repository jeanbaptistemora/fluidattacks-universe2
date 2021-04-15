/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { graphql } from "gatsby";
import React from "react";

import { Home } from "../components/Home";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";

import "modal-video-custom/scss/modal-video.scss";

interface IQueryData {
  data: {
    site: {
      siteMetadata: {
        author: string;
        description: string;
        image: string;
        keywords: string;
        siteUrl: string;
        title: string;
      };
    };
  };
}

const Index: React.FC<IQueryData> = ({ data }: IQueryData): JSX.Element => (
  <React.Fragment>
    <Seo
      author={data.site.siteMetadata.author}
      description={data.site.siteMetadata.description}
      image={`${data.site.siteMetadata.image}`}
      keywords={data.site.siteMetadata.keywords}
      title={data.site.siteMetadata.title}
      url={data.site.siteMetadata.siteUrl}
    />

    <Layout>
      <div>
        <NavbarComponent />

        <Home />
      </div>
    </Layout>
  </React.Fragment>
);

// eslint-disable-next-line import/no-default-export
export default Index;

export const query: void = graphql`
  query {
    site {
      siteMetadata {
        author
        description
        image
        keywords
        siteUrl
        title
      }
    }
  }
`;
