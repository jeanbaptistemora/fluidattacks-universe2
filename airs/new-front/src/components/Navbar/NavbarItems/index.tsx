/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "gatsby";
import { Menu } from "../Menu";
import React from "react";
import { faAngleDown } from "@fortawesome/free-solid-svg-icons";
import * as fluidAttacksLogo from "../../../../static/images/logo-fluid-attacks.png";
import {
  FontAwesomeContainerSmall,
  NavbarContactButton,
  NavbarList,
  NavbarLoginButton,
  NavbarRegularButton,
  NavbarSubcategory,
} from "../../../styles/styledComponents";

const NavbarItems: React.FC = (): JSX.Element => (
  <NavbarList className={"roboto"} id={"navbar_list"}>
    <Menu />

    <li className={"fl"}>
      <Link className={"db tc pa1 no-underline"} to={"/"}>
        <img
          alt={"Fluid Attacks logo navbar"}
          className={"h-5 ml3 pv2"}
          src={fluidAttacksLogo}
        />
      </Link>
    </li>

    <li className={"fr pv4 db-l dn"}>
      <Link className={"no-underline"} to={"/contact-us/"}>
        <NavbarContactButton>{"Contact"}</NavbarContactButton>
      </Link>
    </li>

    <li className={"fr mr3 pr2 pv4 db-l dn"}>
      <Link
        className={"no-underline"}
        to={"https://integrates.fluidattacks.com/"}>
        <NavbarLoginButton>{"Login"}</NavbarLoginButton>
      </Link>
    </li>

    <li className={"fr mr4 pv3 mv1 db-l dn"}>
      <div className={"h3 w1 b--moon-gray br"} />
    </li>

    <li className={"db-xl display-none fr mr3 pv4"}>
      <Link className={"no-underline"} to={"/blog/"}>
        <NavbarRegularButton>{"Blog"}</NavbarRegularButton>
      </Link>
    </li>

    <li className={"db-xl display-none fr mr3 pr2 pv4"}>
      <Link className={"no-underline"} to={"/resources/"}>
        <NavbarRegularButton>{"Resources"}</NavbarRegularButton>
      </Link>
    </li>

    <li className={"db-l dn fr mr3 pr2 pv4 solutions-index"}>
      <Link className={"no-underline"} to={"/solutions/"}>
        <NavbarRegularButton>
          {"Solutions"}
          <FontAwesomeContainerSmall>
            <FontAwesomeIcon icon={faAngleDown} />
          </FontAwesomeContainerSmall>
        </NavbarRegularButton>
      </Link>

      <NavbarSubcategory className={"solutions-content"}>
        <Link className={"f-18 fw4"} to={"/solutions/devsecops/"}>
          {"DevSecOps"}
        </Link>

        <Link className={"f-18 fw4"} to={"/solutions/security-testing/"}>
          {"Security Testing"}
        </Link>

        <Link className={"f-18 fw4"} to={"/solutions/penetration-testing/"}>
          {"Penetration Testing"}
        </Link>

        <Link className={"f-18 fw4"} to={"/solutions/ethical-hacking/"}>
          {"Ethical Hacking"}
        </Link>

        <Link className={"f-18 fw4"} to={"/solutions/red-teaming/"}>
          {"Red Teaming"}
        </Link>

        <Link className={"f-18 fw4"} to={"/solutions/attack-simulation/"}>
          {"Attack Simulation"}
        </Link>

        <Link className={"f-18 fw4"} to={"/solutions/secure-code-review/"}>
          {"Secure Code Review"}
        </Link>

        <Link
          className={"f-18 fw4"}
          to={"/solutions/vulnerability-management/"}>
          {"Vulnerability Management"}
        </Link>
      </NavbarSubcategory>
    </li>

    <li className={"db-l dn fr mr3 pr2 pv4 usecases-index"}>
      <Link className={"no-underline"} to={"/services/continuous-hacking/"}>
        <NavbarRegularButton>
          {"Services"}
          <FontAwesomeContainerSmall>
            <FontAwesomeIcon icon={faAngleDown} />
          </FontAwesomeContainerSmall>
        </NavbarRegularButton>
      </Link>

      <NavbarSubcategory className={"usecases-content"}>
        <Link className={"f-18 fw4"} to={"/services/continuous-hacking/"}>
          {"Continuous Hacking"}
        </Link>

        <Link className={"f-18 fw4"} to={"/services/one-shot-hacking/"}>
          {"One Shot Hacking"}
        </Link>

        <Link className={"f-18 fw4"} to={"/services/comparative/"}>
          {"Comparative"}
        </Link>
      </NavbarSubcategory>
    </li>
  </NavbarList>
);

export { NavbarItems };
