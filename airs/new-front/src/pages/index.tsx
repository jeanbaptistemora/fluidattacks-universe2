/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-namespace:0 */
/* eslint react/jsx-no-bind:0 */
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Layout } from "../components/layout";
import ModalVideo from "modal-video-custom";
import { NavbarComponent } from "../components/navbar";
import React from "react";
import { Seo } from "../components/seo";
import { faArrowRight } from "@fortawesome/free-solid-svg-icons";
import * as playButton from "../assets/images/home/play-video.svg";
import {
  BlackBigHeader,
  BlackBigParagraph,
  BlackSimpleParagraph,
  GetDemoContainer,
  GrayBigParagraph,
  InnerMainContentHome,
  MainContentHome,
  MainCoverHome,
  PlayItButtonContainer,
  PlayItButtonImage,
  PlayItButtonSection,
} from "../styles/styledComponents";
import { Link, graphql } from "gatsby";
import "../assets/scss/index.scss";
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

const Index: React.FC<IQueryData> = ({ data }: IQueryData): JSX.Element => {
  const [isOpen, setOpen] = React.useState(false);
  const handleClose: () => void = (): void => setOpen(false);
  const handleOpen: () => void = (): void => setOpen(true);

  return (
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
                <GetDemoContainer>
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
                </GetDemoContainer>
              </InnerMainContentHome>
            </MainContentHome>
          </MainCoverHome>
          <PlayItButtonSection>
            <ModalVideo
              autoplay={true}
              channel={"youtube"}
              isOpen={isOpen}
              onClose={handleClose}
              videoId={"bT28BUzKPpg"}
            />
            <PlayItButtonContainer onClick={handleOpen}>
              {"PLAY"}
              <PlayItButtonImage src={playButton} />
              {"IT"}
            </PlayItButtonContainer>
          </PlayItButtonSection>
        </div>
      </Layout>
    </React.Fragment>
  );
};

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
