/*
 *There is no danger using dangerouslySetInnerHTML since everything is built in
 *compile time, also
 *Default exports are needed for pages used in nodes by default to create pages
 *like index.tsx or this one
 */
/* eslint react/no-danger:0 */
/* eslint import/no-default-export:0 */
/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { Layout } from "../components/layout";
import { NavbarComponent } from "../components/navbar";
import React from "react";
import { graphql } from "gatsby";

import "tachyons/css/tachyons.min.css";
import "../styles/index.scss";

interface IQueryData {
  data: {
    asciidoc: {
      document: {
        title: string;
      };
      html: string;
      fields: {
        slug: string;
      };
      pageAttributes: {
        slug: string;
      };
    };
  };
}

const DefaultPage: React.FC<IQueryData> = ({
  data,
}: IQueryData): JSX.Element => (
  <React.StrictMode>
    <Layout>
      <div>
        <NavbarComponent />

        <article>
          <h1>{data.asciidoc.document.title}</h1>

          <div dangerouslySetInnerHTML={{ __html: data.asciidoc.html }} />
        </article>
      </div>
    </Layout>
  </React.StrictMode>
);

export default DefaultPage;

export const query: void = graphql`
  query PageArticleBySlug($slug: String!) {
    asciidoc(fields: { slug: { eq: $slug } }) {
      document {
        title
      }
      html
      fields {
        slug
      }
      pageAttributes {
        slug
      }
    }
  }
`;
