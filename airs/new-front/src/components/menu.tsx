/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";

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
      <Link className={"db tc pa1 no-underline"} to={"/"}>
        <img
          alt={"Fluid Attacks logo navbar"}
          className={"h-5 ml3 pv2"}
          src={"../theme/images/logo-fluid-attacks.png"}
        />
      </Link>
    </li>

    <li className={"relative fr pv4 db-l dn"}>
      <Link className={"no-underline"} to={"../contact-us/"}>
        <NavbarContactButton>{"Contact"}</NavbarContactButton>
      </Link>
    </li>

    <li className={"relative fr mr3 pr2 pv4 db-l dn"}>
      <Link
        className={"no-underline"}
        to={"https://integrates.fluidattacks.com/"}>
        <NavbarLoginButton>{"Login"}</NavbarLoginButton>
      </Link>
    </li>

    <li className={"relative fr mr4 pv3 mv1 db-l dn"}>
      <div className={"h3 w1 b--moon-gray br"} />
    </li>

    <li className={"db-xl display-none relative fr mr3 pv4"}>
      <Link className={"no-underline"} to={"../blog/"}>
        <NavbarRegularButton>{"Blog"}</NavbarRegularButton>
      </Link>
    </li>

    <li className={"db-xl display-none relative fr mr3 pr2 pv4"}>
      <Link className={"no-underline"} to={"../resources/"}>
        <NavbarRegularButton>{"Resources"}</NavbarRegularButton>
      </Link>
    </li>

    <li className={"db-l dn fr mr3 pr2 pv4 solutions-index"}>
      <Link className={"no-underline"} to={"../solutions/"}>
        <NavbarRegularButton>{"Solutions"}</NavbarRegularButton>
      </Link>

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
      <Link className={"no-underline"} to={"../services/continuous-hacking/"}>
        <NavbarRegularButton>{"Services"}</NavbarRegularButton>
      </Link>

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
