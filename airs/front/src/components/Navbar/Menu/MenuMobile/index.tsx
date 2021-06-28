/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import { faAngleDown } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "gatsby";
import React from "react";

import {
  ContactButton,
  ContactButtonContainer,
  ContentContainer,
  ContentList,
  FontAwesomeContainerSmall,
  FooterContainer,
  HeaderContainer,
  InnerContentList,
  InnerListContainer,
  InnerListItem,
  ListItem,
  ListItemCheckbox,
  ListItemLabel,
  LogoContainer,
  SidebarContainer,
} from "../../../../styles/styledComponents";
import { CloudImage } from "../../../CloudImage";
import { SocialMedia } from "../../../SocialMedia";

const MenuMobile: React.FC = (): JSX.Element => (
  <SidebarContainer>
    <HeaderContainer>
      <LogoContainer>
        <CloudImage
          alt={"Fluid Attacks Logo Mobile"}
          src={"logo-fluid-mobile"}
        />
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
                    {"Breach and Attack Simulation"}
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
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/about-us/clients/"}
                  >
                    {"Clients"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/about-us/certifications/"}
                  >
                    {"Certifications"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/about-us/differentiators/"}
                  >
                    {"Differentiators"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/about-us/values/"}
                  >
                    {"Values"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/about-us/reviews/"}
                  >
                    {"Reviews"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/about-us/events/"}
                  >
                    {"Events"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"/about-us/people/"}
                  >
                    {"People"}
                  </Link>
                </InnerListItem>
                <InnerListItem>
                  <Link
                    className={
                      "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
                    }
                    to={"https://docs.fluidattacks.com/about/security/"}
                  >
                    {"Security"}
                  </Link>
                </InnerListItem>
              </InnerContentList>
            </InnerListContainer>
          </ListItem>
        </div>
        <ListItem>
          <Link
            className={
              "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
            }
            to={"/blog/"}
          >
            {"Blog"}
          </Link>
        </ListItem>
        <ListItem>
          <Link
            className={
              "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
            }
            to={"/advisories/"}
          >
            {"Advisories"}
          </Link>
        </ListItem>
        <ListItem>
          <Link
            className={
              "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
            }
            to={"/resources/"}
          >
            {"Resources"}
          </Link>
        </ListItem>
        <ListItem>
          <Link
            className={
              "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
            }
            to={"/plans/"}
          >
            {"Plans"}
          </Link>
        </ListItem>
        <ListItem>
          <Link
            className={
              "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
            }
            to={"/careers/"}
          >
            {"Careers"}
          </Link>
        </ListItem>
        <ListItem>
          <Link
            className={
              "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
            }
            to={"/faq/"}
          >
            {"FAQ"}
          </Link>
        </ListItem>
        <ListItem>
          <Link
            className={
              "hv-fluid-rd f5 c-fluid-bk fw4 no-underline menu-txt-trans roboto"
            }
            to={"https://docs.fluidattacks.com/"}
          >
            {"Documentation"}
          </Link>
        </ListItem>
      </ContentList>
    </ContentContainer>
    <FooterContainer>
      <div>
        <ContactButtonContainer>
          <Link
            className={
              "no-underline c-fluid-bk f-key-features menu-txt-trans roboto hv-fluid-rd nt-125"
            }
            to={"/contact-us/"}
          >
            <ContactButton>{"Contact"}</ContactButton>
          </Link>
        </ContactButtonContainer>

        <SocialMedia />
      </div>
    </FooterContainer>
  </SidebarContainer>
);

export { MenuMobile };
