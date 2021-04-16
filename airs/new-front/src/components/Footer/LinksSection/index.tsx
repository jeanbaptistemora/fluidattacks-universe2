/* eslint react/forbid-component-props: 0 */
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
    flex-ns
    justify-center
    justify-around-xl
  `,
})``;

const LinksContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pt4-l
    b
    v-top
    tl
    mh2
    lh-2
  `,
})``;

const LinksSection: React.FC = (): JSX.Element => (
  <FooterMenuContainer>
    <LinksContainer className={"dib-xl"}>
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
    <LinksContainer className={"dib-xl"}>
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
    <LinksContainer className={"dib-xl display-none"}>
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
    <LinksContainer className={"dib-xl display-none"}>
      <HeadLink link={"https://fluidattacks.com/systems/"} name={"Systems"} />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/systems/web-apps/"}
        name={"Web Applications"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/systems/mobile-apps/"}
        name={"Mobile Applications"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/systems/thick-clients/"}
        name={"Thick Clients"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/systems/apis/"}
        name={"APIs and Microservices"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/systems/cloud-infrastructure/"}
        name={"Cloud Infrastructure"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/systems/networks-and-hosts/"}
        name={"Networks and Hosts"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/systems/iot/"}
        name={"Internet of Things"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/systems/ot/"}
        name={"SCADA and OT"}
      />{" "}
      <br />
    </LinksContainer>
    <LinksContainer className={"dib-xl display-none"}>
      <HeadLink
        link={"https://fluidattacks.com/compliance/"}
        name={"Compliance"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/compliance/owasp/"}
        name={"OWASP"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/compliance/pci/"}
        name={"PCI DSS"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/compliance/hipaa/"}
        name={"HIPAA"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/compliance/nist/"}
        name={"NIST"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/compliance/gdpr/"}
        name={"GDPR"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/compliance/cve/"}
        name={"CVE"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/compliance/cwe/"}
        name={"CWE"}
      />{" "}
      <br />
    </LinksContainer>
    <LinksContainer className={"dib-xl display-none"}>
      <HeadLink link={"https://fluidattacks.com/about-us/"} name={"About Us"} />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/about-us/clients/"}
        name={"Clients"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/about-us/certifications/"}
        name={"Certifications"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/about-us/differentiators/"}
        name={"Differentiators"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/about-us/values/"}
        name={"Values"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/about-us/reviews/"}
        name={"Reviews"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/about-us/resources/"}
        name={"Resources"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/about-us/events/"}
        name={"Events"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/about-us/people/"}
        name={"People"}
      />{" "}
      <br />
      <BodyLink
        link={"https://fluidattacks.com/about-us/security/"}
        name={"Security"}
      />{" "}
      <br />
    </LinksContainer>
    <LinksContainer className={"dib-xl"}>
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
      <HeadLink
        link={"https://fluidattacks.com/contact-us/"}
        name={"Contact"}
      />{" "}
      <br />
    </LinksContainer>
  </FooterMenuContainer>
);

export { LinksSection };
