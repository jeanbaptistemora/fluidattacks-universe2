/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { Layout } from "../components/layout";
import { NavbarComponent } from "../components/navbar";
import React from "react";
import { Seo } from "../components/seo";
import { graphql } from "gatsby";
import {
  BlackBigHeader,
  BlackBigParagraph,
  GrayBigParagraph,
  InnerMainContentHome,
  MainContentHome,
  MainCoverHome,
} from "../styles/styledComponents";
import "tachyons/css/tachyons.min.css";
import "../styles/index.scss";

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
        <MainCoverHome>
          <MainContentHome>
            <InnerMainContentHome>
              <BlackBigHeader>{"CONTINUOUS HACKING"}</BlackBigHeader>
              <BlackBigParagraph>{"BY HUMAN EXPERTS"}</BlackBigParagraph>
              <GrayBigParagraph>
                {"FAST, ACCURATE AND COST-EFFECTIVE"}
              </GrayBigParagraph>
            </InnerMainContentHome>
          </MainContentHome>
        </MainCoverHome>
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
