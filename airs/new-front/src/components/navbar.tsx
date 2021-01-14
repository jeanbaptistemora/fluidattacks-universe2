import React from "react";

import {
  MenuButton,
  NavbarContainer,
  NavbarInnerContainer,
  NavbarList,
} from "../styles/styledComponents";

import { MenuDesktop } from "./menu";

export const NavbarComponent: React.FC = (): JSX.Element => (
  <NavbarContainer id={"navbar"}>
    <NavbarInnerContainer id={"inner_navbar"}>
      <NavbarList id={"navbar_list"}>
        <MenuButton>
          <div className={"lower"}>
            <span id="openbtn" className="pointer dib h2-l">
              <img
                className={"w2"}
                src={"/theme/images/menu.svg"}
                alt={"Menu open icon"}
              />
            </span>
          </div>
        </MenuButton>
      </NavbarList>
    </NavbarInnerContainer>
  </NavbarContainer>
);
