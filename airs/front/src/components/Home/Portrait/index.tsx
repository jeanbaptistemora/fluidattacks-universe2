/* eslint react/forbid-component-props: 0 */
/* eslint react/jsx-no-bind:0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import { Link } from "gatsby";
import React from "react";

import {
  GrayBigParagraph,
  HomeImageContainer,
  InnerMainContentHome,
  MainContentHome,
  MainCoverHome,
  NewRegularRedButton,
  PhantomRegularRedButton,
  WhiteBigParagraph,
} from "../../../styles/styledComponents";
import { CloudImage } from "../../CloudImage";

const Portrait: React.FC = (): JSX.Element => {
  const { trackEvent } = useMatomo();

  const matomoEvent = (): void => {
    trackEvent({ action: "product-overview-click", category: "home" });
  };

  return (
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
            <Link className={"no-underline"} to={"/free-trial/"}>
              <NewRegularRedButton className={"mb3 fl mh1 w-auto-ns w-100"}>
                {"Start free trial"}
              </NewRegularRedButton>
            </Link>
            <Link
              className={"no-underline"}
              onClick={matomoEvent}
              to={"/product-overview/"}
            >
              <PhantomRegularRedButton className={"mb3 fl mh1 w-auto-ns w-100"}>
                {"Product overview"}
              </PhantomRegularRedButton>
            </Link>
          </div>
        </InnerMainContentHome>
      </MainContentHome>
    </MainCoverHome>
  );
};

export { Portrait };
