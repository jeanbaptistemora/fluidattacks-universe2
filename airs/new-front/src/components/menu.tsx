import React from "react";

import {
  MenuButton,
  NavbarContactButton,
  NavbarList,
  NavbarLoginButton,
  NavbarRegularButton,
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
    <li className={"relative fr mr3 pr2 pv4 db-l dn"}>
      <a className={"no-underline"}
         href={"https://integrates.fluidattacks.com/"}>
        <NavbarLoginButton>
          Login
        </NavbarLoginButton>
      </a>
    </li>
    <li className={"relative fr mr4 pv3 mv1 db-l dn"}>
      <div className={"h3 w1 b--moon-gray br"}></div>
    </li>
    <li className={"db-xl display-none relative fr mr3 pv4"}>
      <a className={"no-underline"}
         href="../blog/">
        <NavbarRegularButton>
          Blog
        </NavbarRegularButton>
      </a>
    </li>
    <li className={"db-xl display-none relative fr mr3 pr2 pv4"}>
      <a className={"no-underline"}
         href={"../resources/"}>
        <NavbarRegularButton>
          Resources
        </NavbarRegularButton>
      </a>
    </li>
    <li className={"db-l dn fr mr3 pr2 pv4 solutions-index"}>
      <a className={"no-underline"}
          href={"../solutions/"}>
        <NavbarRegularButton>
          Solutions
        </NavbarRegularButton>
      </a>
    </li>
    <li className={"db-l dn fr mr3 pr2 pv4 usecases-index"}>
      <a className={"no-underline"}
          href={"../services/continuous-hacking/"}>
        <NavbarRegularButton>
          Services
        </NavbarRegularButton>
      </a>
    </li>
  </NavbarList>
);
