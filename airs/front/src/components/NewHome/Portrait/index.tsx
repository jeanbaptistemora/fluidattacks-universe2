/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import {
  GrayBigParagraph,
  HomeImageContainer,
  InnerMainContentHome,
  MainContentHome,
  MainCoverHome,
  NewRegularRedButton,
  WhiteBigParagraph,
} from "../../../styles/styledComponents";
import { CloudImage } from "../../CloudImage";

const Portrait: React.FC = (): JSX.Element => (
  <MainCoverHome>
    <MainContentHome>
      <HomeImageContainer>
        <CloudImage
          alt={"Attacks Surface Management"}
          src={"/home/portrait-home.png"}
        />
      </HomeImageContainer>
      <InnerMainContentHome>
        <WhiteBigParagraph className={"f-home-title"}>
          {"Secure your applications with our Continuous Hacking Solution"}
        </WhiteBigParagraph>
        <GrayBigParagraph>
          {"Accurate automation + AI prioritization + Expert intelligence"}
        </GrayBigParagraph>
        <div className={"cf mt4 mb5"}>
          <Link className={"no-underline"} to={"/contact-us-demo/"}>
            <NewRegularRedButton className={"mb3 fl mh1 w-auto-ns w-100"}>
              {"Get a free demo"}
            </NewRegularRedButton>
          </Link>
        </div>
      </InnerMainContentHome>
    </MainContentHome>
  </MainCoverHome>
);

export { Portrait };
