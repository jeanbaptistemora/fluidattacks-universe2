/* eslint react/forbid-component-props: 0 */
import { faArrowRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "gatsby";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { translate } from "../../../utils/translations/translate";

const Container: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-300
    mw-1366
    ph-body
    center
  `,
})``;

const InnerFlexContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    flex-l
  `,
})``;

const ThirdWidthContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  w-34-l
  w-100
  `,
})``;

const Title: StyledComponent<"p", Record<string, unknown>> = styled.p.attrs({
  className: `
    tl
    roboto
    c-black-gray
    fw4
    f5
    mh0
  `,
})``;

const MainText: StyledComponent<"p", Record<string, unknown>> = styled.p.attrs({
  className: `
    neue
    f3
    tl
    fw7
  `,
})``;

const DownloadText: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    t-all-3-eio
    fl
    mv0
  `,
})``;

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
          <FontAwesomeIcon
            className={"c-dkred dib t-all-3-eio mh1"}
            icon={faArrowRight}
          />
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
