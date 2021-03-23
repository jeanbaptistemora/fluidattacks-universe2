/* eslint react/forbid-component-props: 0 */
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "gatsby";
import React from "react";
import { faArrowRight } from "@fortawesome/free-solid-svg-icons";
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
);

export { Portrait };
