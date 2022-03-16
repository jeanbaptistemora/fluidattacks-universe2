/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
import React from "react";

import { BodyLink } from "./BodyLink";
import { HeadLink } from "./HeadLink";

import { CloudImage } from "../../../CloudImage";
import { SocialMedia } from "../../../SocialMedia";
import {
  FlexMenuItems,
  MenuDesktopSectionList,
  MenuSectionContainer,
} from "../../styles/styledComponents";

const MenuDesktop: React.FC = (): JSX.Element => (
  <React.Fragment>
    <FlexMenuItems>
      <MenuSectionContainer>
        <div className={"nowrap"}>
          <MenuDesktopSectionList>
            <HeadLink
              link={"/services/continuous-hacking/"}
              margin={"mb4"}
              name={"Services"}
            />
            <BodyLink
              link={"/services/continuous-hacking/"}
              name={"Continuous Hacking"}
            />
            <BodyLink
              link={"/services/one-shot-hacking/"}
              name={"One-Shot Hacking"}
            />
            <BodyLink link={"/services/comparative/"} name={"Comparative"} />

            <HeadLink link={"/resources/"} margin={"mt4"} name={"Resources"} />
            <BodyLink
              link={"https://docs.fluidattacks.com/criteria/"}
              name={"Criteria"}
            />
          </MenuDesktopSectionList>

          <MenuDesktopSectionList>
            <HeadLink link={"/about-us/"} margin={"mb4"} name={"About Us"} />
            <BodyLink link={"/about-us/clients/"} name={"Clients"} />
            <BodyLink
              link={"/about-us/differentiators/"}
              name={"Differentiators"}
            />
            <BodyLink link={"/about-us/values/"} name={"Values"} />
            <BodyLink link={"/about-us/reviews/"} name={"Reviews"} />
            <BodyLink link={"/resources/"} name={"Resources"} />
            <BodyLink link={"/about-us/events/"} name={"Events"} />
            <BodyLink link={"/about-us/people/"} name={"People"} />
            <BodyLink
              link={"https://docs.fluidattacks.com/about/security/"}
              name={"Security"}
            />
          </MenuDesktopSectionList>
        </div>

        <div className={"nowrap"}>
          <MenuDesktopSectionList>
            <HeadLink link={"/solutions/"} margin={"mb4"} name={"Solutions"} />
            <BodyLink link={"/solutions/devsecops/"} name={"DevSecOps"} />
            <BodyLink
              link={"/solutions/secure-code-review/"}
              name={"Secure Code Review"}
            />
            <BodyLink link={"/solutions/red-teaming/"} name={"Red Teaming"} />
            <BodyLink
              link={"/solutions/attack-simulation/"}
              name={"Breach and Attack Simulation"}
            />
            <BodyLink
              link={"/solutions/security-testing/"}
              name={"Security Testing"}
            />
            <BodyLink
              link={"/solutions/penetration-testing/"}
              name={"Penetration Testing"}
            />
            <BodyLink
              link={"/solutions/ethical-hacking/"}
              name={"Ethical Hacking"}
            />
            <BodyLink
              link={"/solutions/vulnerability-management/"}
              name={"Vulnerability Management"}
            />
          </MenuDesktopSectionList>

          <MenuDesktopSectionList>
            <HeadLink
              link={"/categories/"}
              margin={"mb4"}
              name={"Categories"}
            />
            <BodyLink link={"/categories/sast/"} name={"SAST"} />
            <BodyLink link={"/categories/dast/"} name={"DAST"} />
            <BodyLink link={"/solutions/penetration-testing/"} name={"MPT"} />
            <BodyLink link={"/categories/sca/"} name={"SCA"} />
            <BodyLink link={"/categories/re/"} name={"RE"} />
            <BodyLink link={"/categories/ptaas/"} name={"PTaaS"} />
            <BodyLink link={"/categories/asm/"} name={"ASM"} />
            <BodyLink link={"/solutions/attack-simulation/"} name={"BAS"} />
          </MenuDesktopSectionList>
        </div>

        <div className={"nowrap"}>
          <MenuDesktopSectionList>
            <HeadLink link={"/systems/"} margin={"mb4"} name={"Systems"} />
            <BodyLink link={"/systems/web-apps/"} name={"Web Applications"} />
            <BodyLink
              link={"/systems/mobile-apps/"}
              name={"Mobile Applications"}
            />
            <BodyLink link={"/systems/thick-clients/"} name={"Thick Clients"} />
            <BodyLink link={"/systems/apis/"} name={"APIs and Microservices"} />
            <BodyLink
              link={"/systems/cloud-infrastructure/"}
              name={"Cloud Infrastructure"}
            />
            <BodyLink
              link={"/systems/networks-and-hosts/"}
              name={"Networks and Hosts"}
            />
            <BodyLink link={"/systems/iot/"} name={"Internet of Things"} />
            <BodyLink link={"/systems/ot/"} name={"SCADA and OT"} />
          </MenuDesktopSectionList>

          <MenuDesktopSectionList>
            <HeadLink link={"/plans/"} margin={"mb3"} name={"Plans"} />
            <HeadLink
              link={"/about-us/certifications/"}
              margin={"mb3"}
              name={"Certifications"}
            />
            <HeadLink link={"/blog/"} margin={"mb3"} name={"Blog"} />
            <HeadLink link={"/partners/"} margin={"mb3"} name={"Partners"} />
            <HeadLink link={"/careers/"} margin={"mb3"} name={"Careers"} />
          </MenuDesktopSectionList>
        </div>

        <div className={"nowrap"}>
          <MenuDesktopSectionList>
            <CloudImage
              alt={"Fluid Attacks Logo Menu 2"}
              src={"/airs/menu/overlay-menu"}
            />
          </MenuDesktopSectionList>

          <MenuDesktopSectionList>
            <HeadLink
              link={"/advisories/"}
              margin={"mb3"}
              name={"Advisories"}
            />
            <HeadLink link={"/faq/"} margin={"mb3"} name={"FAQ"} />
            <HeadLink
              link={"https://docs.fluidattacks.com/"}
              margin={"mb3"}
              name={"Documentation"}
            />
            <HeadLink link={"/contact-us/"} margin={"mb3"} name={"Contact"} />
          </MenuDesktopSectionList>
        </div>
      </MenuSectionContainer>
    </FlexMenuItems>
    <div className={"w-100 tc"}>
      <p className={"c-fluid-gray"}>{"FOLLOW US"}</p>
      <SocialMedia />
    </div>
  </React.Fragment>
);

export { MenuDesktop };
