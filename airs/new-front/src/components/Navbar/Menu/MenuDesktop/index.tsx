/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import { Link } from "gatsby";
import React from "react";

import fluidAttacksLogo from "../../../../../static/images/logo-fluid-attacks.png";
import menuSelector from "../../../../../static/images/menu/selector.png";
import { SocialMedia } from "../../../SocialMedia";
import {
  BlackWeightedParagraph,
  FlexMenuItems,
  HalfWidthContainer,
  MenuDesktopSectionList,
  MenuSectionContainer,
  MenuSidebar,
  QuarterHeightContainer,
  SidebarList,
  SidebarListContainer,
  SidebarListItem,
} from "../../styles/navbarStyledComponents";

const MenuDesktop: React.FC = (): JSX.Element => (
  <React.Fragment>
    <FlexMenuItems>
      <HalfWidthContainer>
        <MenuSectionContainer className={"bg-menu-services"}>
          <MenuDesktopSectionList>
            <li className={"mb4"}>
              <Link
                className={"menulink white f3 roboto no-underline nowrap"}
                to={"/services/continuous-hacking/"}
              >
                {"Services"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"/services/continuous-hacking/"}
              >
                {"Continuous Hacking"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"/services/one-shot-hacking/"}
              >
                {"One-Shot Hacking"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"/services/comparative/"}
              >
                {"Comparative"}
              </Link>
            </li>
          </MenuDesktopSectionList>
        </MenuSectionContainer>
        <MenuSectionContainer className={"bg-menu-systems"}>
          <MenuDesktopSectionList>
            <li className={"mb4"}>
              <Link
                className={"menulink white f3 roboto no-underline nowrap"}
                to={"https://fluidattacks.com/systems/"}
              >
                {"Systems"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/systems/web-apps/"}
              >
                {"Web Applications"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/systems/mobile-apps/"}
              >
                {"Mobile Applications"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/systems/thick-clients/"}
              >
                {"Thick Clients"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/systems/apis/"}
              >
                {"API's and Microservices"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/systems/cloud-infrastructure/"}
              >
                {"Cloud Infrastructure"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/systems/networks-and-hosts/"}
              >
                {"Networks and Hosts"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/systems/iot/"}
              >
                {"Internet of Things"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/systems/ot/"}
              >
                {"SCADA and OT"}
              </Link>
            </li>
          </MenuDesktopSectionList>
        </MenuSectionContainer>
      </HalfWidthContainer>
      <HalfWidthContainer>
        <MenuSectionContainer className={"bg-menu-solutions"}>
          <MenuDesktopSectionList>
            <li className={"mb4"}>
              <Link
                className={"menulink white f3 roboto no-underline nowrap"}
                to={"/solutions/"}
              >
                {"Solutions"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"/solutions/devsecops/"}
              >
                {"DevSecOps"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"/solutions/security-testing/"}
              >
                {"Security Testing"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"/solutions/penetration-testing/"}
              >
                {"Penetration Testing"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"/solutions/ethical-hacking/"}
              >
                {"Ethical Hacking"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"/solutions/red-teaming/"}
              >
                {"Red Teaming"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"/solutions/attack-simulation/"}
              >
                {"Attack Simulation"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"/solutions/secure-code-review/"}
              >
                {"Secure Code Review"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"/solutions/vulnerability-management/"}
              >
                {"Vulnerability Management"}
              </Link>
            </li>
          </MenuDesktopSectionList>
        </MenuSectionContainer>
        <MenuSectionContainer className={"bg-menu-aboutus"}>
          <MenuDesktopSectionList>
            <li className={"mb4"}>
              <Link
                className={"menulink white f3 roboto no-underline nowrap"}
                to={"https://fluidattacks.com/about-us/"}
              >
                {"About Us"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/about-us/clients/"}
              >
                {"Clients"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/about-us/differentiators/"}
              >
                {"Differentiators"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/about-us/values/"}
              >
                {"Values"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/about-us/reviews/"}
              >
                {"Reviews"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/about-us/resources/"}
              >
                {"Resources"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/about-us/events/"}
              >
                {"Events"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/about-us/people/"}
              >
                {"People"}
              </Link>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"https://fluidattacks.com/about-us/security/"}
              >
                {"Security"}
              </Link>
            </li>
          </MenuDesktopSectionList>
        </MenuSectionContainer>
      </HalfWidthContainer>
    </FlexMenuItems>
    <MenuSidebar>
      <QuarterHeightContainer>
        <img alt={"Fluid Attacks Logo Menu"} src={fluidAttacksLogo} />
      </QuarterHeightContainer>
      <SidebarListContainer>
        <SidebarList>
          <SidebarListItem>
            <Link
              className={"c-fluid-bk roboto no-underline nowrap hv-fluid-rd"}
              to={"https://fluidattacks.com/blog/"}
            >
              {"Blog"}
            </Link>
          </SidebarListItem>
          <SidebarListItem>
            <Link
              className={"c-fluid-bk roboto no-underline nowrap hv-fluid-rd"}
              to={"https://fluidattacks.com/partners/"}
            >
              {"Partners"}
            </Link>
          </SidebarListItem>
          <SidebarListItem>
            <Link
              className={"c-fluid-bk roboto no-underline nowrap hv-fluid-rd"}
              to={"https://fluidattacks.com/careers/"}
            >
              {"Careers"}
            </Link>
          </SidebarListItem>
          <SidebarListItem>
            <Link
              className={"c-fluid-bk roboto no-underline nowrap hv-fluid-rd"}
              to={"https://fluidattacks.com/advisories/"}
            >
              {"Advisories"}
            </Link>
          </SidebarListItem>
          <SidebarListItem>
            <Link
              className={"c-fluid-bk roboto no-underline nowrap hv-fluid-rd"}
              to={"https://fluidattacks.com/plans/"}
            >
              {"Plans"}
            </Link>
          </SidebarListItem>
          <SidebarListItem>
            <Link
              className={"c-fluid-bk roboto no-underline nowrap hv-fluid-rd"}
              to={"https://fluidattacks.com/faq/"}
            >
              {"FAQ"}
            </Link>
          </SidebarListItem>
          <SidebarListItem>
            <a
              className={"c-fluid-bk roboto no-underline nowrap hv-fluid-rd"}
              href={"https://community.fluidattacks.com/"}
            >
              {"Community"}
            </a>
          </SidebarListItem>
          <SidebarListItem>
            <Link
              className={"c-fluid-bk roboto no-underline nowrap hv-fluid-rd"}
              to={"https://fluidattacks.com/contact-us/"}
            >
              {"Contact"}
            </Link>
          </SidebarListItem>
        </SidebarList>
      </SidebarListContainer>
      <QuarterHeightContainer>
        <div className={"w-100 tc"}>
          <BlackWeightedParagraph>
            {"FOLLOW FLUID ATTACKS"}
            <em>
              <img alt={"Menu Selctor"} src={menuSelector} />
            </em>
          </BlackWeightedParagraph>

          <SocialMedia />
        </div>
      </QuarterHeightContainer>
    </MenuSidebar>
  </React.Fragment>
);

export { MenuDesktop };
