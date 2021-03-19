/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
/* eslint react/jsx-no-bind:0 */
import { Link } from "gatsby";
import { SocialMedia } from "../../SocialMedia";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import * as closeMenuIcon from "../../../../static/images/cross.png";
import * as fluidAttacksLogo from "../../../../static/images/logo-fluid-attacks.png";
import * as menuSelector from "../../../../static/images/menu/selector.png";
import {
  BlackWeightedParagraph,
  CloseMenuButton,
  CloseMenuButtonContainer,
  FlexMenuItems,
  HalfWidthContainer,
  MenuInnerContainer,
  MenuSectionContainer,
  MenuSectionList,
  MenuSidebar,
  QuarterHeightContainer,
  SidebarList,
  SidebarListContainer,
  SidebarListItem,
} from "../styles/navbarStyledComponents";
import {
  CenteredMaxWidthContainer,
  MenuButton,
} from "../../../styles/styledComponents";
import React, { useState } from "react";

const MenuContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    db-l
    dn
  `,
})``;

const Menu: React.FC = (): JSX.Element => {
  const [isOpen, setIsOpen] = useState(false);
  function toggle(): void {
    setIsOpen(!isOpen);
  }

  return (
    <React.Fragment>
      <MenuButton onClick={toggle}>
        <div className={"lower"}>
          <span className={"pointer dib h2-l"} id={"openbtn"}>
            <img
              alt={"Menu open icon"}
              className={"w2"}
              src={"https://fluidattacks.com/theme/images/menu.svg"}
            />
          </span>
        </div>
      </MenuButton>
      <MenuContainer>
        <MenuInnerContainer className={isOpen ? "" : "dn"} id={"mySidenavXl"}>
          <CenteredMaxWidthContainer className={"flex"}>
            <CloseMenuButtonContainer>
              <CloseMenuButton onClick={toggle}>
                <img
                  alt={"Close Menu Icon"}
                  className={"w2"}
                  src={closeMenuIcon}
                />
              </CloseMenuButton>
            </CloseMenuButtonContainer>
            <FlexMenuItems>
              <HalfWidthContainer>
                <MenuSectionContainer className={"bg-menu-services"}>
                  <MenuSectionList>
                    <li className={"mb4"}>
                      <Link
                        className={
                          "menulink white f3 roboto no-underline nowrap"
                        }
                        to={"/services/continuous-hacking/"}>
                        {"Services"}
                      </Link>
                    </li>
                    <li className={"mv1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/services/continuous-hacking/"}>
                        {"Continuous Hacking"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/services/one-shot-hacking/"}>
                        {"One-Shot Hacking"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/services/comparative/"}>
                        {"Comparative"}
                      </Link>
                    </li>
                  </MenuSectionList>
                </MenuSectionContainer>
                <MenuSectionContainer className={"bg-menu-systems"}>
                  <MenuSectionList>
                    <li className={"mb4"}>
                      <Link
                        className={
                          "menulink white f3 roboto no-underline nowrap"
                        }
                        to={"/systems/"}>
                        {"Systems"}
                      </Link>
                    </li>
                    <li className={"mv1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/systems/web-apps/"}>
                        {"Web Applications"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/systems/mobile-apps/"}>
                        {"Mobile Applications"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/systems/thick-clients/"}>
                        {"Thick Clients"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/systems/apis/"}>
                        {"API's and Microservices"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/systems/cloud-infrastructure/"}>
                        {"Cloud Infrastructure"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/systems/networks-and-hosts/"}>
                        {"Networks and Hosts"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/systems/iot/"}>
                        {"Internet of Things"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/systems/ot/"}>
                        {"SCADA and OT"}
                      </Link>
                    </li>
                  </MenuSectionList>
                </MenuSectionContainer>
              </HalfWidthContainer>
              <HalfWidthContainer>
                <MenuSectionContainer className={"bg-menu-solutions"}>
                  <MenuSectionList>
                    <li className={"mb4"}>
                      <Link
                        className={
                          "menulink white f3 roboto no-underline nowrap"
                        }
                        to={"/solutions/"}>
                        {"Solutions"}
                      </Link>
                    </li>
                    <li className={"mv1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/solutions/devsecops/"}>
                        {"DevSecOps"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/solutions/security-testing/"}>
                        {"Security Testing"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/solutions/penetration-testing/"}>
                        {"Penetration Testing"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/solutions/ethical-hacking/"}>
                        {"Ethical Hacking"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/solutions/red-teaming/"}>
                        {"Red Teaming"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/solutions/attack-simulation/"}>
                        {"Attack Simulation"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/solutions/secure-code-review/"}>
                        {"Secure Code Review"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/solutions/vulnerability-management/"}>
                        {"Vulnerability Management"}
                      </Link>
                    </li>
                  </MenuSectionList>
                </MenuSectionContainer>
                <MenuSectionContainer className={"bg-menu-aboutus"}>
                  <MenuSectionList>
                    <li className={"mb4"}>
                      <Link
                        className={
                          "menulink white f3 roboto no-underline nowrap"
                        }
                        to={"/about-us/"}>
                        {"About Us"}
                      </Link>
                    </li>
                    <li className={"mv1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/about-us/clients/"}>
                        {"Clients"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/about-us/differentiators/"}>
                        {"Differentiators"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/about-us/values/"}>
                        {"Values"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/about-us/reviews/"}>
                        {"Reviews"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/about-us/resources/"}>
                        {"Resources"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/about-us/events/"}>
                        {"Events"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/about-us/people/"}>
                        {"People"}
                      </Link>
                    </li>
                    <li className={"m1"}>
                      <Link
                        className={"menulink white roboto no-underline nowrap"}
                        to={"/about-us/security/"}>
                        {"Security"}
                      </Link>
                    </li>
                  </MenuSectionList>
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
                      className={
                        "c-fluid-bk roboto no-underline nowrap hv-fluid-rd"
                      }
                      to={"/blog/"}>
                      {"Blog"}
                    </Link>
                  </SidebarListItem>
                  <SidebarListItem>
                    <Link
                      className={
                        "c-fluid-bk roboto no-underline nowrap hv-fluid-rd"
                      }
                      to={"/partners/"}>
                      {"Partners"}
                    </Link>
                  </SidebarListItem>
                  <SidebarListItem>
                    <Link
                      className={
                        "c-fluid-bk roboto no-underline nowrap hv-fluid-rd"
                      }
                      to={"/careers/"}>
                      {"Careers"}
                    </Link>
                  </SidebarListItem>
                  <SidebarListItem>
                    <Link
                      className={
                        "c-fluid-bk roboto no-underline nowrap hv-fluid-rd"
                      }
                      to={"/advisories/"}>
                      {"Advisories"}
                    </Link>
                  </SidebarListItem>
                  <SidebarListItem>
                    <Link
                      className={
                        "c-fluid-bk roboto no-underline nowrap hv-fluid-rd"
                      }
                      to={"/plans/"}>
                      {"Plans"}
                    </Link>
                  </SidebarListItem>
                  <SidebarListItem>
                    <Link
                      className={
                        "c-fluid-bk roboto no-underline nowrap hv-fluid-rd"
                      }
                      to={"/faq/"}>
                      {"FAQ"}
                    </Link>
                  </SidebarListItem>
                  <SidebarListItem>
                    <a
                      className={
                        "c-fluid-bk roboto no-underline nowrap hv-fluid-rd"
                      }
                      href={"https://community.fluidattacks.com/"}>
                      {"Community"}
                    </a>
                  </SidebarListItem>
                  <SidebarListItem>
                    <Link
                      className={
                        "c-fluid-bk roboto no-underline nowrap hv-fluid-rd"
                      }
                      to={"/contact-us/"}>
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
          </CenteredMaxWidthContainer>
        </MenuInnerContainer>
      </MenuContainer>
    </React.Fragment>
  );
};

export { Menu };
