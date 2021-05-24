import { Link } from "gatsby";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { CardButton } from "../BlogsList/StyledComponents";

const MainDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    vh-100
    thank-you-bg
    items-center
    justify-center
    flex
    bg-center
  `,
})``;
const InnerDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    tc
  `,
})``;
const TitleDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    roboto
    c-fluid-bk
    f2
    fw7
    tc
    lh-solid
  `,
})``;
const ContentMainDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w36-l
    center
  `,
})``;
const ContentInnerDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    roboto
    f4
    c-fluid-bk
    fw3
    tc
  `,
})``;
const ButtonDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    dib
    tc
    w-100-s
    w-100-m
    pv3
  `,
})``;

const ThankYouContent: React.FC<{ content: string; title: string }> = ({
  content,
  title,
}: {
  content: string;
  title: string;
}): JSX.Element => {
  return (
    <MainDiv>
      <InnerDiv>
        <TitleDiv>{title}</TitleDiv>
        <ContentMainDiv>
          <ContentInnerDiv
            dangerouslySetInnerHTML={{
              __html: content,
            }}
          />

          <ButtonDiv>
            <Link to={"/blog/"}>
              <CardButton>{"Read Last Blog Entry"}</CardButton>
            </Link>
          </ButtonDiv>
        </ContentMainDiv>
      </InnerDiv>
    </MainDiv>
  );
};

export { ThankYouContent };
