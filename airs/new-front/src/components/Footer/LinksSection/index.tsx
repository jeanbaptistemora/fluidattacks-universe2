import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { BodyLink } from "./BodyLink";
import { HeadLink } from "./HeadLink";

const FooterMenuContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pb4
    w-100
    tc
    nowrap
    flex
    justify-around
  `,
})``;

const LinksContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pt4-l
    b
    dib-xl
    display-none
    v-top
    tl
    mh2
    lh-2
  `,
})``;

const LinksSection: React.FC = (): JSX.Element => (
  <FooterMenuContainer>
    <LinksContainer>
      <HeadLink link={"/services/continuous-hacking/"} name={"Services"} />{" "}
      <br />
      <BodyLink
        link={"/services/continuous-hacking/"}
        name={"Continuous Hacking"}
      />{" "}
      <br />
      <BodyLink
        link={"/services/one-shot-hacking/"}
        name={"One-shot Hacking"}
      />{" "}
      <br />
      <BodyLink link={"/services/comparative/"} name={"Comparative"} /> <br />
    </LinksContainer>
    <LinksContainer>
      <HeadLink link={"/solutions/"} name={"Solutions"} /> <br />
      <BodyLink link={"/solutions/devsecops/"} name={"DevSecOps"} /> <br />
      <BodyLink
        link={"/solutions/security-testing/"}
        name={"Security Testing"}
      />{" "}
      <br />
      <BodyLink
        link={"/solutions/penetration-testing/"}
        name={"Penetration Testing"}
      />{" "}
      <br />
      <BodyLink
        link={"/solutions/ethical-hacking/"}
        name={"Ethical Hacking"}
      />{" "}
      <br />
      <BodyLink link={"/solutions/red-teaming/"} name={"Red Teaming"} /> <br />
      <BodyLink
        link={"/solutions/attack-simulation/"}
        name={"Attack Simulation"}
      />{" "}
      <br />
      <BodyLink
        link={"/solutions/secure-code-review/"}
        name={"Secure Code Review"}
      />{" "}
      <br />
      <BodyLink
        link={"/solutions/vulnerability-management/"}
        name={"Vulnerability Management"}
      />{" "}
      <br />
    </LinksContainer>
    <LinksContainer>
      <HeadLink
        link={"https://fluidattacks.com/categories/"}
        name={"Categories"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/categories/sast/"}
        name={"SAST"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/categories/dast/"}
        name={"DAST"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/categories/penetration-testing/"}
        name={"MPT"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/categories/sca/"}
        name={"SCA"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/categories/re/"}
        name={"RE"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/categories/ptaas/"}
        name={"PTaaS"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/categories/asm/"}
        name={"ASM"}
      />{" "}
      <br />
    </LinksContainer>
    <LinksContainer>
      <HeadLink link={"/systems/"} name={"Systems"} /> <br />
      <BodyLink link={"/systems/web-apps/"} name={"Web Applications"} /> <br />
      <BodyLink
        link={"/systems/mobile-apps/"}
        name={"Mobile Applications"}
      />{" "}
      <br />
      <BodyLink link={"/systems/thick-clients/"} name={"Thick Clients"} />{" "}
      <br />
      <BodyLink link={"/systems/apis/"} name={"APIs and Microservices"} />{" "}
      <br />
      <BodyLink
        link={"/systems/cloud-infrastructure/"}
        name={"Cloud Infrastructure"}
      />{" "}
      <br />
      <BodyLink
        link={"/systems/networks-and-hosts/"}
        name={"Networks and Hosts"}
      />{" "}
      <br />
      <BodyLink link={"/systems/iot/"} name={"Internet of Things"} /> <br />
      <BodyLink link={"/systems/ot/"} name={"SCADA and OT"} /> <br />
    </LinksContainer>
    <LinksContainer>
      <HeadLink link={"/compliance/"} name={"Compliance"} /> <br />
      <BodyLink link={"/compliance/owasp/"} name={"OWASP"} /> <br />
      <BodyLink link={"/compliance/pci/"} name={"PCI"} /> <br />
      <BodyLink link={"/compliance/hipaa/"} name={"HIPAA"} /> <br />
      <BodyLink link={"/compliance/nist/"} name={"NIST"} /> <br />
      <BodyLink link={"/compliance/gdpr/"} name={"GDPR"} /> <br />
    </LinksContainer>
    <LinksContainer>
      <HeadLink link={"/about-us/"} name={"About Us"} /> <br />
      <BodyLink link={"/about-us/clients/"} name={"Clients"} /> <br />
      <BodyLink
        link={"/about-us/certifications/"}
        name={"Certifications"}
      />{" "}
      <br />
      <BodyLink
        link={"/about-us/differentiators/"}
        name={"Differentiators"}
      />{" "}
      <br />
      <BodyLink link={"/about-us/values/"} name={"Values"} /> <br />
      <BodyLink link={"/about-us/reviews/"} name={"Reviews"} /> <br />
      <BodyLink link={"/about-us/resources/"} name={"Resources"} /> <br />
      <BodyLink link={"/about-us/events/"} name={"Events"} /> <br />
      <BodyLink link={"/about-us/people/"} name={"People"} /> <br />
      <BodyLink link={"/about-us/security/"} name={"Security"} /> <br />
    </LinksContainer>
    <LinksContainer>
      <HeadLink link={"/blog/"} name={"Blog"} /> <br />
      <HeadLink link={"/partners/"} name={"Partners"} /> <br />
      <HeadLink link={"/careers/"} name={"Careers"} /> <br />
      <HeadLink link={"/advisories/"} name={"Advisories"} /> <br />
      <HeadLink link={"/faq/"} name={"FAQ"} /> <br />
      <HeadLink
        link={"https://community.fluidattacks.com/"}
        name={"Community"}
      />{" "}
      <br />
      <HeadLink link={"/contact-us/"} name={"Contact"} /> <br />
      <HeadLink link={"/newsletter/"} name={"Newsletter"} /> <br />
    </LinksContainer>
  </FooterMenuContainer>
);

export { LinksSection };
