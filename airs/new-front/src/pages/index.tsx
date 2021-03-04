/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Layout } from "../components/layout";
import { NavbarComponent } from "../components/navbar";
import React from "react";
import { Seo } from "../components/seo";
import { faArrowRight } from "@fortawesome/free-solid-svg-icons";
import {
  BlackBigHeader,
  BlackBigParagraph,
  BlackSimpleParagraph,
  GrayBigParagraph,
  InnerMainContentHome,
  MainContentHome,
  MainCoverHome,
} from "../styles/styledComponents";
import { Link, graphql } from "gatsby";
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
              <div className={"w-80-l ba b--light-gray pa4 mt4"}>
                <BlackSimpleParagraph className={"mb2"}>
                  {
                    "Security should not be an obstacle in the time-to-market of \
                    your application. With Continuous Hacking, we integrate security \
                    testing into your software development lifecycles."
                  }
                </BlackSimpleParagraph>
                <Link
                  className={"roboto f5 c-fluid-bk fw3 no-underline"}
                  to={"/contact-us/"}>
                  {"Get a Demo"}
                  <FontAwesomeIcon
                    className={"c-dkred mh1 dib"}
                    icon={faArrowRight}
                  />
                </Link>
              </div>
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
