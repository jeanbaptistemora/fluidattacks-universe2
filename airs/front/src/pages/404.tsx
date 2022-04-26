/* eslint import/no-default-export:0 */

import { Link } from "gatsby";
import React from "react";

import { NavbarComponent } from "../components/Navbar";
import {
  ButtonContainer,
  ErrorContainer,
  ErrorDescription,
  ErrorSection,
  ErrorTitle,
  RegularRedButton,
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
            <RegularRedButton>{"Go Home"}</RegularRedButton>
          </Link>
        </ButtonContainer>
      </ErrorContainer>
    </ErrorSection>
  </React.Fragment>
);

export default Error404Page;
