/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import { Link } from "gatsby";
import React from "react";

import { CloudImage } from "../../../CloudImage";
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
              <a
                className={"menulink white f3 roboto no-underline nowrap"}
                href={"/systems/"}
              >
                {"Systems"}
              </a>
            </li>
            <li className={"mv1"}>
              <a
                className={"menulink white roboto no-underline nowrap"}
                href={"/systems/web-apps/"}
              >
                {"Web Applications"}
              </a>
            </li>
            <li className={"mv1"}>
              <Link
                className={"menulink white roboto no-underline nowrap"}
                to={"/systems/mobile-apps/"}
              >
                {"Mobile Applications"}
              </Link>
            </li>
            <li className={"mv1"}>
              <a
                className={"menulink white roboto no-underline nowrap"}
                href={"/systems/thick-clients/"}
              >
                {"Thick Clients"}
              </a>
            </li>
            <li className={"mv1"}>
              <a
                className={"menulink white roboto no-underline nowrap"}
                href={"/systems/apis/"}
              >
                {"API's and Microservices"}
              </a>
            </li>
            <li className={"mv1"}>
              <a
                className={"menulink white roboto no-underline nowrap"}
                href={"/systems/cloud-infrastructure/"}
              >
                {"Cloud Infrastructure"}
              </a>
            </li>
            <li className={"mv1"}>
              <a
                className={"menulink white roboto no-underline nowrap"}
                href={"/systems/networks-and-hosts/"}
              >
                {"Networks and Hosts"}
              </a>
            </li>
            <li className={"mv1"}>
              <a
                className={"menulink white roboto no-underline nowrap"}
                href={"/systems/iot/"}
              >
                {"Internet of Things"}
              </a>
            </li>
            <li className={"mv1"}>
              <a
                className={"menulink white roboto no-underline nowrap"}
                href={"/systems/ot/"}
              >
                {"SCADA and OT"}
              </a>
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
              <a
                className={"menulink white f3 roboto no-underline nowrap"}
                href={"https://fluidattacks.com/about-us/"}
              >
                {"About Us"}
              </a>
            </li>
            <li className={"mv1"}>
              <a
                className={"menulink white roboto no-underline nowrap"}
                href={"https://fluidattacks.com/about-us/clients/"}
              >
                {"Clients"}
              </a>
            </li>
            <li className={"mv1"}>
              <a
                className={"menulink white roboto no-underline nowrap"}
                href={"https://fluidattacks.com/about-us/differentiators/"}
              >
                {"Differentiators"}
              </a>
            </li>
            <li className={"mv1"}>
              <a
                className={"menulink white roboto no-underline nowrap"}
                href={"https://fluidattacks.com/about-us/values/"}
              >
                {"Values"}
              </a>
            </li>
            <li className={"mv1"}>
              <a
                className={"menulink white roboto no-underline nowrap"}
                href={"https://fluidattacks.com/about-us/reviews/"}
              >
                {"Reviews"}
              </a>
            </li>
            <li className={"mv1"}>
              <a
                className={"menulink white roboto no-underline nowrap"}
                href={"/resources/"}
              >
                {"Resources"}
              </a>
            </li>
            <li className={"mv1"}>
              <a
                className={"menulink white roboto no-underline nowrap"}
                href={"https://fluidattacks.com/about-us/events/"}
              >
                {"Events"}
              </a>
            </li>
            <li className={"mv1"}>
              <a
                className={"menulink white roboto no-underline nowrap"}
                href={"https://fluidattacks.com/about-us/people/"}
              >
                {"People"}
              </a>
            </li>
          </MenuDesktopSectionList>
        </MenuSectionContainer>
      </HalfWidthContainer>
    </FlexMenuItems>
    <MenuSidebar>
      <QuarterHeightContainer>
        <CloudImage
          alt={"Fluid Attacks Logo Menu"}
          src={"logo-fluid-attacks-light"}
        />
      </QuarterHeightContainer>
      <SidebarListContainer>
        <SidebarList>
          <SidebarListItem>
            <a
              className={"c-fluid-bk roboto no-underline nowrap hv-fluid-rd"}
              href={"/plans/"}
            >
              {"Plans"}
            </a>
          </SidebarListItem>
          <SidebarListItem>
            <Link
              className={"c-fluid-bk roboto no-underline nowrap hv-fluid-rd"}
              to={"https://fluidattacks.com/blog/"}
            >
              {"Blog"}
            </Link>
          </SidebarListItem>
          <SidebarListItem>
            <a
              className={"c-fluid-bk roboto no-underline nowrap hv-fluid-rd"}
              href={"/partners/"}
            >
              {"Partners"}
            </a>
          </SidebarListItem>
          <SidebarListItem>
            <a
              className={"c-fluid-bk roboto no-underline nowrap hv-fluid-rd"}
              href={"/careers/"}
            >
              {"Careers"}
            </a>
          </SidebarListItem>
          <SidebarListItem>
            <a
              className={"c-fluid-bk roboto no-underline nowrap hv-fluid-rd"}
              href={"/advisories/"}
            >
              {"Advisories"}
            </a>
          </SidebarListItem>
          <SidebarListItem>
            <a
              className={"c-fluid-bk roboto no-underline nowrap hv-fluid-rd"}
              href={"/faq/"}
            >
              {"FAQ"}
            </a>
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
            <a
              className={"c-fluid-bk roboto no-underline nowrap hv-fluid-rd"}
              href={"/contact-us/"}
            >
              {"Contact"}
            </a>
          </SidebarListItem>
        </SidebarList>
      </SidebarListContainer>
      <QuarterHeightContainer>
        <div className={"w-100 tc"}>
          <BlackWeightedParagraph>
            {"FOLLOW FLUID ATTACKS"}
            <em>
              <CloudImage alt={"Menu Selctor"} src={"menu/selector"} />
            </em>
          </BlackWeightedParagraph>

          <SocialMedia />
        </div>
      </QuarterHeightContainer>
    </MenuSidebar>
  </React.Fragment>
);

export { MenuDesktop };
