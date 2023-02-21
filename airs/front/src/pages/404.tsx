/* eslint import/no-default-export:0 */

import { Link } from "gatsby";
import React from "react";

import { NavbarComponent } from "../scenes/Menu";
import {
  ButtonContainer,
  ErrorContainer,
  ErrorDescription,
  ErrorSection,
  ErrorTitle,
  NewRegularRedButton,
} from "../styles/styledComponents";

const Error404Page: React.FC = (): JSX.Element => (
  <React.Fragment>
    <NavbarComponent />
    <ErrorSection>
      <ErrorContainer>
        <ErrorTitle>{"404"}</ErrorTitle>
        <ErrorDescription>{"Whoops! Nothing Found"}</ErrorDescription>
        <ButtonContainer>
          <Link to={"/"}>
            <NewRegularRedButton>{"Go Home"}</NewRegularRedButton>
          </Link>
        </ButtonContainer>
      </ErrorContainer>
    </ErrorSection>
  </React.Fragment>
);

export default Error404Page;
