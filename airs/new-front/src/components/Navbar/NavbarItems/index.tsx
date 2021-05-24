/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
import { faAngleDown } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "gatsby";
import React from "react";

import {
  FontAwesomeContainerSmall,
  NavbarContactButton,
  NavbarList,
  NavbarLoginButton,
  NavbarRegularButton,
  NavbarSubcategory,
} from "../../../styles/styledComponents";
import { CloudImage } from "../../CloudImage";
import { Search } from "../../Search";
import { Menu } from "../Menu";

const searchIndices = [
  { name: `fluidattacks_airs`, title: `fluidattacks_airs` },
];

const NavbarItems: React.FC = (): JSX.Element => (
  <NavbarList className={"roboto"} id={"navbar_list"}>
    <Menu />

    <li className={"fl"}>
      <Link className={"db tc pa1 no-underline"} to={"/"}>
        <CloudImage
          alt={"Fluid Attacks logo navbar"}
          src={"logo-fluid-attacks-light"}
          styles={"h-5 ml3 pv2"}
        />
      </Link>
    </li>

    <li className={"fr pv4 db-l dn"}>
      <Link className={"no-underline"} to={"/contact-us/"}>
        <NavbarContactButton>{"Contact"}</NavbarContactButton>
      </Link>
    </li>

    <li className={"fr mr3 pr2 pv4 db-l dn"}>
      <Link className={"no-underline"} to={"https://app.fluidattacks.com/"}>
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

    <Search indices={searchIndices} />

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
          to={"/solutions/vulnerability-management/"}
        >
          {"Vulnerability Management"}
        </Link>
      </NavbarSubcategory>
    </li>

    <li className={"db-l dn fr mr3 pr2 pv4 services-index"}>
      <Link className={"no-underline"} to={"/services/continuous-hacking/"}>
        <NavbarRegularButton>
          {"Services"}
          <FontAwesomeContainerSmall>
            <FontAwesomeIcon icon={faAngleDown} />
          </FontAwesomeContainerSmall>
        </NavbarRegularButton>
      </Link>

      <NavbarSubcategory className={"services-content"}>
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
