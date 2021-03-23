/* eslint react/forbid-component-props: 0 */
/* eslint import/no-namespace:0 */
/* eslint react/jsx-no-bind:0 */
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "gatsby";
import ModalVideo from "modal-video-custom";
import { faArrowRight } from "@fortawesome/free-solid-svg-icons";
import * as playButton from "../../../static/images/home/play-video.svg";
import {
  BlackBigHeader,
  BlackBigParagraph,
  BlackSimpleParagraph,
  FlexCenterItemsContainer,
  GetDemoContainer,
  GrayBigParagraph,
  InnerMainContentHome,
  MainContentHome,
  MainCoverHome,
  PlayItButtonContainer,
  PlayItButtonImage,
} from "../../styles/styledComponents";
import React, { useState } from "react";

const Home: React.FC = (): JSX.Element => {
  const [isOpen, setOpen] = useState(false);
  function handleClose(): void {
    setOpen(false);
  }

  function handleOpen(): void {
    setOpen(true);
  }

  return (
    <React.Fragment>
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
                to={"/contact-us/"}
              >
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
      <FlexCenterItemsContainer className={"h-section"}>
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
      </FlexCenterItemsContainer>
    </React.Fragment>
  );
};

export { Home };
