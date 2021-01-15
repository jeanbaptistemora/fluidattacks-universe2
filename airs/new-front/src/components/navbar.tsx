import React from "react";

import { NavbarItems } from "../components/menu";
import {
  MenuButton,
  NavbarContainer,
  NavbarInnerContainer,
} from "../styles/styledComponents";

export const NavbarComponent: React.FC = (): JSX.Element => (
  <NavbarContainer id={"navbar"}>
    <NavbarInnerContainer id={"inner_navbar"}>
      <NavbarItems>

      </NavbarItems>
    </NavbarInnerContainer>
  </NavbarContainer>
);
