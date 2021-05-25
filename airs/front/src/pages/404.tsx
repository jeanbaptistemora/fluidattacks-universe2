/* eslint import/no-default-export:0 */

import { Link } from "gatsby";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { RegularRedButton } from "../styles/styledComponents";

const Error404Page: React.FC = (): JSX.Element => {
  const ErrorSection: StyledComponent<
    "section",
    Record<string, unknown>
  > = styled.section.attrs({
    className: `
      error-bg
      vh-100
      w-100
      cover
      bg-top
      flex
      items-center
      justify-center
    `,
  })``;
  const ErrorContainer: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
      flex
      flex-column
      justify-between
    `,
  })``;
  const ErrorTitle: StyledComponent<
    "h1",
    Record<string, unknown>
  > = styled.h1.attrs({
    className: `
      neue
      c-fluid-bk
      f-error
      fw7
      tc
      lh-solid
      ma0
    `,
  })``;
  const ErrorDescription: StyledComponent<
    "p",
    Record<string, unknown>
  > = styled.p.attrs({
    className: `
      neue
      c-fluid-bk
      f2
      fw7
      tc
      ma0
    `,
  })``;
  const ButtonContainer: StyledComponent<
    "h1",
    Record<string, unknown>
  > = styled.h1.attrs({
    className: `
      tc
      mt3
    `,
  })``;

  return (
    <ErrorSection>
      <ErrorContainer>
        <ErrorTitle>{"404"}</ErrorTitle>
        <ErrorDescription>{"Whoops! Nothing Found"}</ErrorDescription>
        <ButtonContainer>
          <Link to={"/"}>
            <RegularRedButton>{"Go Home"}</RegularRedButton>
          </Link>
        </ButtonContainer>
      </ErrorContainer>
    </ErrorSection>
  );
};

export default Error404Page;
