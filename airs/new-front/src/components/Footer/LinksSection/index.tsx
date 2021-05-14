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
      <HeadLink link={"/categories/"} name={"Categories"} /> <br />
      <BodyLink link={"/categories/sast/"} name={"SAST"} /> <br />
      <BodyLink link={"/categories/dast/"} name={"DAST"} /> <br />
      <BodyLink link={"/solutions/penetration-testing/"} name={"MPT"} /> <br />
      <BodyLink link={"/categories/sca/"} name={"SCA"} /> <br />
      <BodyLink link={"/categories/re/"} name={"RE"} /> <br />
      <BodyLink link={"/categories/ptaas/"} name={"PTaaS"} /> <br />
      <BodyLink link={"/categories/asm/"} name={"ASM"} /> <br />
    </LinksContainer>
    <LinksContainer className={"dib-xl display-none"}>
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
    <LinksContainer className={"dib-xl display-none"}>
      <HeadLink link={"/compliance/"} name={"Compliance"} /> <br />
      <BodyLink link={"/compliance/owasp/"} name={"OWASP"} /> <br />
      <BodyLink link={"/compliance/pci/"} name={"PCI DSS"} /> <br />
      <BodyLink link={"/compliance/hipaa/"} name={"HIPAA"} /> <br />
      <BodyLink link={"/compliance/nist/"} name={"NIST"} /> <br />
      <BodyLink link={"/compliance/gdpr/"} name={"GDPR"} /> <br />
      <BodyLink link={"/compliance/cve/"} name={"CVE"} /> <br />
      <BodyLink link={"/compliance/cwe/"} name={"CWE"} /> <br />
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
      <BodyLink link={"/resources/"} name={"Resources"} /> <br />
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
    </LinksContainer>
    <LinksContainer className={"dib-xl"}>
      <HeadLink link={"https://fluidattacks.com/blog/"} name={"Blog"} /> <br />
      <HeadLink link={"/partners/"} name={"Partners"} /> <br />
      <HeadLink link={"/careers/"} name={"Careers"} /> <br />
      <HeadLink link={"/advisories/"} name={"Advisories"} /> <br />
      <HeadLink link={"https://fluidattacks.com/faq/"} name={"FAQ"} /> <br />
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
