/* eslint react/forbid-component-props: 0 */
import { FontAwesomeContainerSmall } from "../../../styles/styledComponents";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import { faAngleLeft, faAngleRight } from "@fortawesome/free-solid-svg-icons";

const Container: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-700
    mw-1366
    ph-body
    center
    flex
  `,
})``;

const QuarterWidthContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-25-l
  `,
})``;

const TitleVertical: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    tl
    rotate-180
    roboto
    c-black-gray
    f5
    ma0
    wm-tb-rl
  `,
})``;

const ArrowButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    bg-transparent
    bn
    pa3
    dib
  `,
})``;

const SolutionsSection: React.FC = (): JSX.Element => (
  <Container>
    <QuarterWidthContainer>
      <TitleVertical>{"SOLUTIONS"}</TitleVertical>
    </QuarterWidthContainer>
    <QuarterWidthContainer className={"db-l dn"}>
      <ArrowButton>
        <FontAwesomeContainerSmall>
          <FontAwesomeIcon className={"f3"} icon={faAngleLeft} />
        </FontAwesomeContainerSmall>
      </ArrowButton>
      <ArrowButton>
        <FontAwesomeContainerSmall>
          <FontAwesomeIcon className={"f3"} icon={faAngleRight} />
        </FontAwesomeContainerSmall>
      </ArrowButton>
    </QuarterWidthContainer>
  </Container>
);

export { SolutionsSection };
