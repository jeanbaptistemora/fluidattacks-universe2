import React from "react";

import { NavbarItems } from "./NavbarItems";

import {
  NavbarContainer,
  NavbarInnerContainer,
} from "../../styles/styledComponents";

export const NavbarComponent: React.FC = (): JSX.Element => (
  <NavbarContainer id={"navbar"}>
    <NavbarInnerContainer id={"inner_navbar"}>
      <NavbarItems />
    </NavbarInnerContainer>
  </NavbarContainer>
);
