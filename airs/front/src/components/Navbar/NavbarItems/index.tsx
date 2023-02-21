/* eslint react/jsx-no-bind:0 */
/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import { Link } from "gatsby";
import React, { useCallback } from "react";
import { IoIosArrowDown } from "react-icons/io";

import {
  IconContainerSmall,
  NavbarItem,
  NavbarList,
  NavbarRegularButton,
  NavbarSubcategory,
} from "../../../styles/styledComponents";
import { AirsLink } from "../../AirsLink";
import { Button } from "../../Button";
import { CloudImage } from "../../CloudImage";
import { Container } from "../../Container";
import { Menu } from "../Menu";

const NavbarItems: React.FC = (): JSX.Element => {
  const { trackEvent } = useMatomo();

  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({ action: "free-trial-click", category: "navbar" });
  }, [trackEvent]);

  return (
    <NavbarList className={"poppins"} id={"navbar_list"}>
      <div className={"w-auto flex flex-nowrap"}>
        <Menu />
        <li>
          <Link className={"db tc pa1 no-underline"} to={"/"}>
            <Container ml={3} pv={2} width={"160px"}>
              <CloudImage
                alt={"Fluid Attacks logo navbar"}
                src={"logo-fluid-2022"}
              />
            </Container>
          </Link>
        </li>
      </div>
      <div className={"w-auto dn flex-l center"}>
        <NavbarItem className={"db-l dn solutions-index"}>
          <Link className={"no-underline"} to={"/solutions/"}>
            <NavbarRegularButton>
              {"Solutions"}
              <IconContainerSmall>
                <IoIosArrowDown />
              </IconContainerSmall>
            </NavbarRegularButton>
          </Link>

          <NavbarSubcategory className={"solutions-content nl-5"}>
            <Link className={"f-18 fw4"} to={"/solutions/devsecops/"}>
              {"DevSecOps"}
            </Link>
            <Link className={"f-18 fw4"} to={"/solutions/secure-code-review/"}>
              {"Secure Code Review"}
            </Link>
            <Link className={"f-18 fw4"} to={"/solutions/red-teaming/"}>
              {"Red Teaming"}
            </Link>
            <Link className={"f-18 fw4"} to={"/solutions/attack-simulation/"}>
              {"Breach and Attack Simulation"}
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
            <Link
              className={"f-18 fw4"}
              to={"/solutions/vulnerability-management/"}
            >
              {"Vulnerability Management"}
            </Link>
          </NavbarSubcategory>
        </NavbarItem>
        <NavbarItem className={"db-l dn"}>
          <Link className={"no-underline"} to={"/certifications/"}>
            <NavbarRegularButton>{"Certifications"}</NavbarRegularButton>
          </Link>
        </NavbarItem>
        <NavbarItem className={"db-xl display-none"}>
          <Link className={"no-underline"} to={"/resources/"}>
            <NavbarRegularButton>{"Resources"}</NavbarRegularButton>
          </Link>
        </NavbarItem>
        <NavbarItem className={"db-xl display-none"}>
          <Link className={"no-underline"} to={"/plans/"}>
            <NavbarRegularButton>{"Plans"}</NavbarRegularButton>
          </Link>
        </NavbarItem>
        <NavbarItem className={"db-xl display-none"}>
          <Link className={"no-underline"} to={"/advisories/"}>
            <NavbarRegularButton>{"Advisories"}</NavbarRegularButton>
          </Link>
        </NavbarItem>
        <NavbarItem className={"db-xl display-none"}>
          <Link className={"no-underline"} to={"/blog/"}>
            <NavbarRegularButton>{"Blog"}</NavbarRegularButton>
          </Link>
        </NavbarItem>
      </div>
      <div className={"w-auto flex-l flex-nowrap dn"}>
        <li className={"mr3 pv4 db-l dn"}>
          <AirsLink href={"https://app.fluidattacks.com/"}>
            <NavbarRegularButton className={"b fw7"}>
              {"Log in"}
            </NavbarRegularButton>
          </AirsLink>
        </li>

        <li className={"mr3 pv4 db-l dn"}>
          <AirsLink href={"/contact-us/"}>
            <Button variant={"tertiary"}>{"Contact now"}</Button>
          </AirsLink>
        </li>

        <li className={"pv4"}>
          <AirsLink href={"/free-trial/"}>
            <Button onClick={matomoFreeTrialEvent} variant={"primary"}>
              {"Start free trial"}
            </Button>
          </AirsLink>
        </li>
      </div>
    </NavbarList>
  );
};

export { NavbarItems };
