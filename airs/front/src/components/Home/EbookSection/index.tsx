/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import { RiArrowRightLine } from "react-icons/ri";

import {
  Container,
  DownloadText,
  InnerFlexContainer,
  MainText,
  ThirdWidthContainer,
  Title,
} from "./styledComponents";

import { translate } from "../../../utils/translations/translate";

const EbookSection: React.FC = (): JSX.Element => (
  <Container>
    <Title>{"EBOOK"}</Title>
    <InnerFlexContainer>
      <ThirdWidthContainer className={"ml0-l mr-auto-l"}>
        <MainText className={"c-fluid-bk"}>
          {translate.t("ebook.question")}
        </MainText>
        <Link
          className={
            "demo-button roboto f5 c-fluid-bk fw4 no-underline t-all-3-eio"
          }
          to={"https://landing.fluidattacks.com/us/ebook/"}
        >
          <DownloadText>{translate.t("ebook.download")}</DownloadText>
          <RiArrowRightLine className={"c-dkred dib t-all-3-eio mh1"} />
        </Link>
      </ThirdWidthContainer>
      <ThirdWidthContainer className={"db-l dn mr0 ml-auto"}>
        <MainText className={"c-fluid-gray tr"}>
          {translate.t("ebook.phrase")}
        </MainText>
      </ThirdWidthContainer>
    </InnerFlexContainer>
  </Container>
);

export { EbookSection };
