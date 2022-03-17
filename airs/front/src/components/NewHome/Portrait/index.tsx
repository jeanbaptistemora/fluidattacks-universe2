/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import {
  HomeImageContainer,
  MainContentHome,
  NewGrayBigParagraph,
  NewInnerMainContentHome,
  NewMainCoverHome,
  NewRegularRedButton,
  WhiteBigParagraph,
} from "../../../styles/styledComponents";
import { CloudImage } from "../../CloudImage";

const Portrait: React.FC = (): JSX.Element => (
  <NewMainCoverHome>
    <MainContentHome>
      <HomeImageContainer>
        <CloudImage alt={"portrait-home"} src={"/home/portrait-home.png"} />
      </HomeImageContainer>
      <NewInnerMainContentHome>
        <WhiteBigParagraph className={"f-home-title"}>
          {"Secure your application with our Continuous Hacking Solution"}
        </WhiteBigParagraph>
        <NewGrayBigParagraph>
          {"Effective Automation + IA + Expert Intelligence"}
        </NewGrayBigParagraph>
        <div className={"cf mt4 mb5"}>
          <Link className={"no-underline"} to={"/contact-us/"}>
            <NewRegularRedButton className={"mb3 fl mh1 w-auto-ns w-100"}>
              {"Get a free demo"}
            </NewRegularRedButton>
          </Link>
        </div>
      </NewInnerMainContentHome>
    </MainContentHome>
  </NewMainCoverHome>
);

export { Portrait };
