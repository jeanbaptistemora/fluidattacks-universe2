/* eslint react/forbid-component-props: 0 */
import { faArrowRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "gatsby";
import React from "react";
import ScrollAnimation from "react-animate-on-scroll";

import {
  BlackBigHeader,
  BlackBigParagraph,
  BlackSimpleParagraph,
  GetDemoContainer,
  GrayBigParagraph,
  InnerMainContentHome,
  MainContentHome,
  MainCoverHome,
} from "../../../styles/styledComponents";

const Portrait: React.FC = (): JSX.Element => (
  <MainCoverHome>
    <MainContentHome>
      <InnerMainContentHome>
        <ScrollAnimation animateIn={"animate__fadeInDown"} animateOnce={true}>
          <BlackBigHeader>{"CONTINUOUS HACKING"}</BlackBigHeader>
          <BlackBigParagraph>{"BY HUMAN EXPERTS"}</BlackBigParagraph>
          <GrayBigParagraph>
            {"FAST, ACCURATE AND COST-EFFECTIVE"}
          </GrayBigParagraph>
        </ScrollAnimation>
        <GetDemoContainer>
          <BlackSimpleParagraph className={"mb2"}>
            {
              "Security should not be an obstacle in the time-to-market of \
              your application. With Continuous Hacking, we integrate security \
              testing into your software development lifecycles."
            }
          </BlackSimpleParagraph>
          <Link
            className={
              "demo-button roboto f5 c-fluid-bk fw3 no-underline t-all-3-eio"
            }
            to={"https://fluidattacks.com/contact-us/"}
          >
            <p className={"fl ma0 t-all-3-eio"}>{"Get a Demo"}</p>
            <FontAwesomeIcon
              className={"c-dkred dib t-all-3-eio mh1"}
              icon={faArrowRight}
            />
          </Link>
        </GetDemoContainer>
      </InnerMainContentHome>
    </MainContentHome>
  </MainCoverHome>
);

export { Portrait };
