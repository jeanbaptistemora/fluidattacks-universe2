/* eslint-disable-next-line react/forbid-component-props */
import React from "react";

import {
  MenuButton,
  NavbarContactButton,
  NavbarList,
  NavbarLoginButton,
  NavbarRegularButton,
  NavbarSubcategory,
  SubcategoryLink,
} from "../styles/styledComponents";

export const NavbarItems: React.FC = (): JSX.Element => (
  //eslint-disable-next-line react/forbid-component-props
  <NavbarList className={"roboto"} id={"navbar_list"}>
    <MenuButton>
      <div className={"lower"}>
        <span className={"pointer dib h2-l"} id={"openbtn"}>
          <img
            alt={"Menu open icon"}
            className={"w2"}
            src={"../theme/images/menu.svg"}
          />
        </span>
      </div>
    </MenuButton>

    <li className={"fl"}>
      <a className={"db tc pa1 no-underline"} href={"/"}>
        <img
          alt={"Fluid Attacks logo navbar"}
          className={"h-5 ml3 pv2"}
          src={"../theme/images/fluid-attacks-logo.webp"}
        />
      </a>
    </li>

    <li className={"relative fr pv4 db-l dn"}>
      <a className={"no-underline"} href={"../contact-us/"}>
        <NavbarContactButton>{"Contact"}</NavbarContactButton>
      </a>
    </li>

    <li className={"relative fr mr3 pr2 pv4 db-l dn"}>
      <a
        className={"no-underline"}
        href={"https://integrates.fluidattacks.com/"}>
        <NavbarLoginButton>{"Login"}</NavbarLoginButton>
      </a>
    </li>

    <li className={"relative fr mr4 pv3 mv1 db-l dn"}>
      <div className={"h3 w1 b--moon-gray br"} />
    </li>

    <li className={"db-xl display-none relative fr mr3 pv4"}>
      <a className={"no-underline"} href={"../blog/"}>
        <NavbarRegularButton>{"Blog"}</NavbarRegularButton>
      </a>
    </li>

    <li className={"db-xl display-none relative fr mr3 pr2 pv4"}>
      <a className={"no-underline"} href={"../resources/"}>
        <NavbarRegularButton>{"Resources"}</NavbarRegularButton>
      </a>
    </li>

    <li className={"db-l dn fr mr3 pr2 pv4 solutions-index"}>
      <a className={"no-underline"} href={"../solutions/"}>
        <NavbarRegularButton>{"Solutions"}</NavbarRegularButton>
      </a>

      <NavbarSubcategory
        //eslint-disable-next-line react/forbid-component-props
        className={"solutions-content"}>
        <SubcategoryLink href={"../solutions/devsecops/"}>
          {"DevSecOps"}
        </SubcategoryLink>

        <SubcategoryLink href={"../solutions/security-testing/"}>
          {"Security Testing"}
        </SubcategoryLink>

        <SubcategoryLink href={"../solutions/penetration-testing/"}>
          {"Penetration Testing"}
        </SubcategoryLink>

        <SubcategoryLink href={"../solutions/ethical-hacking/"}>
          {"Ethical Hacking"}
        </SubcategoryLink>

        <SubcategoryLink href={"../solutions/red-teaming/"}>
          {"Red Teaming"}
        </SubcategoryLink>

        <SubcategoryLink href={"../solutions/attack-simulation/"}>
          {"Attack Simulation"}
        </SubcategoryLink>

        <SubcategoryLink href={"../solutions/secure-code-review/"}>
          {"Secure Code Review"}
        </SubcategoryLink>

        <SubcategoryLink href={"../solutions/vulnerability-management/"}>
          {"Vulnerability Management"}
        </SubcategoryLink>
      </NavbarSubcategory>
    </li>

    <li className={"db-l dn fr mr3 pr2 pv4 usecases-index"}>
      <a className={"no-underline"} href={"../services/continuous-hacking/"}>
        <NavbarRegularButton>{"Services"}</NavbarRegularButton>
      </a>

      <NavbarSubcategory
        //eslint-disable-next-line react/forbid-component-props
        className={"usecases-content"}>
        <SubcategoryLink href={"../services/continuous-hacking/"}>
          {"Continuous Hacking"}
        </SubcategoryLink>

        <SubcategoryLink href={"../services/one-shot-hacking/"}>
          {"One Shot Hacking"}
        </SubcategoryLink>

        <SubcategoryLink href={"../services/comparative/"}>
          {"Comparative"}
        </SubcategoryLink>
      </NavbarSubcategory>
    </li>
  </NavbarList>
);
