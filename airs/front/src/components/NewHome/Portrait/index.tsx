/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

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
        <CloudImage alt={"portrait-home"} src={"/home/portrait-home.png"} />
      </HomeImageContainer>
      <NewInnerMainContentHome>
        <WhiteBigParagraph className={"f-home-title"}>
          {"Secure your application with our Continuous Hacking Solution."}
        </WhiteBigParagraph>
        <NewGrayBigParagraph>
          {"Effective Automation + IA + Expert Intelligence"}
        </NewGrayBigParagraph>
        <GrayMediumParagraph>{`"Quote"`}</GrayMediumParagraph>
        <GrayLittleParagraph>{`Name, position, company`}</GrayLittleParagraph>
        <div className={"cf mt4 mb5"}>
          <Link className={"no-underline"} to={"https://app.fluidattacks.com/"}>
            <NewRegularRedButton className={"mb3 fl mh1 w-auto-ns w-100"}>
              {"Get a free demo"}
            </NewRegularRedButton>
          </Link>
          <Link className={"no-underline"} to={"/newHome"}>
            <PhantomRegularRedButton className={"fl mh1 w-auto-ns w-100"}>
              {"Contact an expert"}
            </PhantomRegularRedButton>
          </Link>
        </div>
      </NewInnerMainContentHome>
    </MainContentHome>
  </NewMainCoverHome>
);

export { Portrait };
