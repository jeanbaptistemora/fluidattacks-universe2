/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import ScrollAnimation from "react-animate-on-scroll";

import {
  GrayLittleParagraph,
  GrayMediumParagraph,
  HomeImageContainer,
  MainContentHome,
  NewGrayBigParagraph,
  NewInnerMainContentHome,
  NewMainCoverHome,
  NewRegularRedButton,
  PhantomRegularRedButton,
  WhiteBigParagraph,
} from "../../../styles/styledComponents";
import { CloudImage } from "../../CloudImage";

const Portrait: React.FC = (): JSX.Element => (
  <NewMainCoverHome>
    <MainContentHome>
      <HomeImageContainer>
        <ScrollAnimation animateIn={"animate__fadeInDown"} animateOnce={true}>
          <CloudImage alt={"portrait-home"} src={"/home/portrait-home.png"} />
        </ScrollAnimation>
      </HomeImageContainer>
      <NewInnerMainContentHome>
        <ScrollAnimation animateIn={"animate__fadeInDown"} animateOnce={true}>
          <WhiteBigParagraph>
            {"Secure your application with our Continuous Hacking Solution."}
          </WhiteBigParagraph>
          <NewGrayBigParagraph>
            {"Effective Automation + IA + Expert Intelligence"}
          </NewGrayBigParagraph>
          <GrayMediumParagraph>
            {`"Overall we like and enjoy the experience and the service.`}
            <br />
            {`The more we use it the more value we get from it."`}
          </GrayMediumParagraph>
          <GrayLittleParagraph>
            {`Andrew Chung, VP of Information Technology at GESA `}
          </GrayLittleParagraph>
          <Link className={"no-underline"} to={"/newHome"}>
            <NewRegularRedButton className={"mv3 fl mh1 w-auto-ns w-100"}>
              {"Start your free trial"}
            </NewRegularRedButton>
          </Link>
          <Link className={"no-underline"} to={"/newHome"}>
            <PhantomRegularRedButton
              className={"mt3-ns mb5  fl mh1 w-auto-ns w-100"}
            >
              {"Product overview"}
            </PhantomRegularRedButton>
          </Link>
        </ScrollAnimation>
      </NewInnerMainContentHome>
    </MainContentHome>
  </NewMainCoverHome>
);

export { Portrait };
