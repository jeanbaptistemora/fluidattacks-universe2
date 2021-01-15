import React from "react";

import {
  MenuButton,
  NavbarContactButton,
  NavbarList,
} from "../styles/styledComponents";

export const NavbarItems: React.FC = (): JSX.Element => (
  <NavbarList id={"navbar_list"} className={"roboto"}>
    <MenuButton>
      <div className={"lower"}>
        <span id="openbtn" className="pointer dib h2-l">
          <img
            className={"w2"}
            src={"../theme/images/menu.svg"}
            alt={"Menu open icon"}
          />
        </span>
      </div>
    </MenuButton>
    <li className={"fl"}>
      <a className={"db tc pa1 no-underline"} href={"/"}>
        <img
          className={"h-5 ml3 pv2"}
          src={"../theme/images/fluid-attacks-logo.png"}
          alt={"Fluid Attacks logo navbar"} />
      </a>
    </li>
    <li className={"relative fr pv4 db-l dn"}>
      <a className={"no-underline"} href={"../contact-us/"}>
        <NavbarContactButton>
          Contact
        </NavbarContactButton>
      </a>
    </li>
  </NavbarList>
);
