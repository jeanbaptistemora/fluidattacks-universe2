/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import { faAngleDown } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "gatsby";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import fluidAttacksLogoMobile from "../../../../../static/images/logo-fluid-mobile.png";
import { FontAwesomeContainerSmall } from "../../../../styles/styledComponents";
import { SocialMedia } from "../../../SocialMedia";

const SidebarContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    bg-white
    overflow-y-auto
    mw5
    nowrap
  `,
})``;

const HeaderContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    min-h-25
  `,
})``;

const LogoContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    tl
    pa3
  `,
})``;

const ContentContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pl4
    overflow-y-auto
    h-50
  `,
})``;

const ContentList: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
    list
    ma0
    pa0
    tl
  `,
})``;

const ListItem: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
    db
    pb3
    pr3
  `,
})``;

const ListItemCheckbox: StyledComponent<
  "input",
  Record<string, unknown>
> = styled.input.attrs({
  className: `
    dn
  `,
  type: "checkbox",
})``;

const ListItemLabel: StyledComponent<
  "label",
  Record<string, unknown>
> = styled.label.attrs({
  className: `
    pointer
    hv-fluid-rd
    f5
    c-fluid-bk
    fw4
    t-color-2
    roboto
  `,
})``;

const InnerListContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pv2
  `,
})`
  display: none;
`;

const InnerContentList: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
    list
    pl3
  `,
})``;

const InnerListItem: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
    pv2
  `,
})``;

const FooterContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    justify-center
    items-center
    flex
    min-h-25
  `,
})``;

const ContactButtonContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    tl
    pb3
    ph3
  `,
})``;

const ContactButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    outline-transparent
    fw7
    f-18
    br2
    bw1
    ph5
    pv2
    bg-white
    bc-fluid-red
    ba
    hv-fluid-rd
    hv-bd-fluid-red
    t-all-3-eio
    c-dkred
    pointer
  `,
})``;

const MenuMobile: React.FC = (): JSX.Element => (
  <SidebarContainer>
    <HeaderContainer>
      <LogoContainer>
        <img alt={"Fluid Attacks Logo Mobile"} src={fluidAttacksLogoMobile} />
      </LogoContainer>
    </HeaderContainer>
    <ContentContainer>
      <ContentList>
        <div>
          <ListItem>
            <ListItemCheckbox
              className={"services-title"}
              id={"services-title"}
              name={"services"}
            />
            <ListItemLabel htmlFor={"services-title"}>
              {"Services"}
              <FontAwesomeContainerSmall>
                <FontAwesomeIcon icon={faAngleDown} />
              </FontAwesomeContainerSmall>
            </ListItemLabel>
            <InnerListContainer className={"services-list"}>
              <InnerContentList>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/services/continuous-hacking/"}
                  >
                    {"Continuous Hacking"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/services/one-shot-hacking/"}
                  >
                    {"One-Shot Hacking"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/services/comparative/"}
                  >
                    {"Comparative"}
                  </Link>
                </InnerListItem>
              </InnerContentList>
            </InnerListContainer>
          </ListItem>
        </div>
        <div>
          <ListItem>
            <ListItemCheckbox
              className={"solutions-title"}
              id={"solutions-title"}
              name={"solutions"}
            />
            <ListItemLabel htmlFor={"solutions-title"}>
              {"Solutions"}
              <FontAwesomeContainerSmall>
                <FontAwesomeIcon icon={faAngleDown} />
              </FontAwesomeContainerSmall>
            </ListItemLabel>
            <InnerListContainer className={"solutions-list"}>
              <InnerContentList>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/solutions/devsecops/"}
                  >
                    {"DevSecOps"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/solutions/security-testing/"}
                  >
                    {"Security Testing"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/solutions/penetration-testing/"}
                  >
                    {"Penetration Testing"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/solutions/ethical-hacking/"}
                  >
                    {"Ethical Hacking"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/solutions/red-teaming/"}
                  >
                    {"Red Teaming"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/solutions/attack-simulation/"}
                  >
                    {"Attack Simulation"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/solutions/secure-code-review/"}
                  >
                    {"Secure Code Review"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/solutions/vulnerability-management/"}
                  >
                    {"Vulnerability Management"}
                  </Link>
                </InnerListItem>
              </InnerContentList>
            </InnerListContainer>
          </ListItem>
        </div>
        <div>
          <ListItem>
            <ListItemCheckbox
              className={"aboutus-title"}
              id={"aboutus-title"}
              name={"aboutus"}
            />
            <ListItemLabel htmlFor={"aboutus-title"}>
              {"About Us"}
              <FontAwesomeContainerSmall>
                <FontAwesomeIcon icon={faAngleDown} />
              </FontAwesomeContainerSmall>
            </ListItemLabel>
            <InnerListContainer className={"aboutus-list"}>
              <InnerContentList>
                <InnerListItem>
                  <a
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    href={"https://fluidattacks.com/about-us/clients/"}
                  >
                    {"Clients"}
                  </a>
                </InnerListItem>
                <InnerListItem>
                  <a
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    href={"https://fluidattacks.com/about-us/certifications/"}
                  >
                    {"Certifications"}
                  </a>
                </InnerListItem>
                <InnerListItem>
                  <a
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    href={"https://fluidattacks.com/about-us/differentiators/"}
                  >
                    {"Differentiators"}
                  </a>
                </InnerListItem>
                <InnerListItem>
                  <a
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    href={"https://fluidattacks.com/about-us/values/"}
                  >
                    {"Values"}
                  </a>
                </InnerListItem>
                <InnerListItem>
                  <a
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    href={"https://fluidattacks.com/about-us/reviews/"}
                  >
                    {"Reviews"}
                  </a>
                </InnerListItem>
                <InnerListItem>
                  <a
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    href={"https://fluidattacks.com/about-us/events/"}
                  >
                    {"Events"}
                  </a>
                </InnerListItem>
                <InnerListItem>
                  <a
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    href={"https://fluidattacks.com/about-us/people/"}
                  >
                    {"People"}
                  </a>
                </InnerListItem>
                <InnerListItem>
                  <a
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    href={"https://fluidattacks.com/about-us/security/"}
                  >
                    {"Security"}
                  </a>
                </InnerListItem>
              </InnerContentList>
            </InnerListContainer>
          </ListItem>
        </div>
        <ListItem>
          <a
            className={
              "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
            }
            href={"https://fluidattacks.com/blog/"}
          >
            {"Blog"}
          </a>
        </ListItem>
        <ListItem>
          <a
            className={
              "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
            }
            href={"https://fluidattacks.com/advisories/"}
          >
            {"Advisories"}
          </a>
        </ListItem>
        <ListItem>
          <a
            className={
              "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
            }
            href={"https://fluidattacks.com/resources/"}
          >
            {"Resources"}
          </a>
        </ListItem>
        <ListItem>
          <a
            className={
              "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
            }
            href={"https://fluidattacks.com/plans/"}
          >
            {"Plans"}
          </a>
        </ListItem>
        <ListItem>
          <a
            className={
              "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
            }
            href={"https://fluidattacks.com/careers/"}
          >
            {"Careers"}
          </a>
        </ListItem>
        <ListItem>
          <a
            className={
              "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
            }
            href={"https://fluidattacks.com/faq/"}
          >
            {"FAQ"}
          </a>
        </ListItem>
        <ListItem>
          <a
            className={
              "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
            }
            href={"https://community.fluidattacks.com/"}
          >
            {"Community"}
          </a>
        </ListItem>
      </ContentList>
    </ContentContainer>
    <FooterContainer>
      <div>
        <ContactButtonContainer>
          <a
            className={
              "no-underline c-fluid-bk f-key-features menu-txt-trans roboto hv-fluid-rd nt-125"
            }
            href={"https://fluidattacks.com/contact-us/"}
          >
            <ContactButton>{"Contact"}</ContactButton>
          </a>
        </ContactButtonContainer>

        <SocialMedia />
      </div>
    </FooterContainer>
  </SidebarContainer>
);

export { MenuMobile };
