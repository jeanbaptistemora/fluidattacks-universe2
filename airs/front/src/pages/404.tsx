/* eslint import/no-default-export:0 */

import { Link } from "gatsby";
import React from "react";

import {
  ButtonContainer,
  ErrorContainer,
  ErrorDescription,
  ErrorSection,
  ErrorTitle,
  RegularRedButton,
} from "../styles/styledComponents";

const Error404Page: React.FC = (): JSX.Element => (
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

export default Error404Page;
