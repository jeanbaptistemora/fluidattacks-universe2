/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { graphql } from "gatsby";
import React from "react";

import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Home } from "../components/NewHome";
import { Seo } from "../components/Seo";

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
          "https://res.cloudinary.com/fluid-attacks/image/upload/c_scale,w_1200/v1622583388/airs/logo_fluid_attacks_2021_eqop3k.png"
        }
        keywords={keywords}
        title={title}
        url={siteUrl}
      />

      <Layout>
        <div>
          <NavbarComponent />

          <Home />
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default NewHomeIndex;

export const query: void = graphql`
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
