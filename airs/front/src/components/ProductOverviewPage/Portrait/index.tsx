/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import {
  InnerMainContentPortrait,
  MainContentPortrait,
  PortraitBigParagraph,
  PortraitContainer,
  PortraitImageContainer,
  PortraitParagraph,
} from "./styledComponents";

import { translate } from "../../../utils/translations/translate";
import { CloudImage } from "../../CloudImage";
import { BigRegularRedButton } from "../styledComponents";

const Portrait: React.FC = (): JSX.Element => (
  <PortraitContainer>
    <MainContentPortrait>
      <InnerMainContentPortrait>
        <PortraitBigParagraph>
          {translate.t("productOverview.portrait.title")}
        </PortraitBigParagraph>
        <PortraitParagraph>
          {translate.t("productOverview.portrait.paragraph")}
        </PortraitParagraph>
        <div className={"cf tl-l tc mt4 mb5"}>
          <Link className={"no-underline"} to={"/contact-us-demo/"}>
            <BigRegularRedButton>
              {translate.t("productOverview.mainButton")}
            </BigRegularRedButton>
          </Link>
        </div>
      </InnerMainContentPortrait>
      <PortraitImageContainer>
        <CloudImage
          alt={"Attacks Surface Management Vulns"}
          src={"/product-overview/portrait/product-overview-portrait.png"}
        />
      </PortraitImageContainer>
    </MainContentPortrait>
  </PortraitContainer>
);

export { Portrait };
