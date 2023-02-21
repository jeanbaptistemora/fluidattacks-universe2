/* eslint react/forbid-component-props: 0 */
import React from "react";

import { BodyLink } from "./BodyLink";
import { HeadLink } from "./HeadLink";

import {
  FooterMenuContainer,
  LinksContainer,
} from "../styles/styledComponents";

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
    </LinksContainer>
    <LinksContainer className={"dib-xl"}>
      <HeadLink link={"/solutions/"} name={"Solutions"} /> <br />
      <BodyLink link={"/solutions/devsecops/"} name={"DevSecOps"} /> <br />
      <BodyLink
        link={"/solutions/secure-code-review/"}
        name={"Secure Code Review"}
      />{" "}
      <br />
      <BodyLink link={"/solutions/red-teaming/"} name={"Red Teaming"} /> <br />
      <BodyLink
        link={"/solutions/attack-simulation/"}
        name={"Breach and Attack Simulation"}
      />{" "}
      <br />
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
      <BodyLink
        link={"/solutions/vulnerability-management/"}
        name={"Vulnerability Management"}
      />{" "}
      <br />
    </LinksContainer>
    <LinksContainer className={"dib-xl display-none"}>
      <HeadLink link={"/product/"} name={"Categories"} /> <br />
      <BodyLink link={"/product/sast/"} name={"SAST"} /> <br />
      <BodyLink link={"/product/dast/"} name={"DAST"} /> <br />
      <BodyLink link={"/solutions/penetration-testing/"} name={"MPT"} /> <br />
      <BodyLink link={"/product/sca/"} name={"SCA"} /> <br />
      <BodyLink link={"/product/re/"} name={"RE"} /> <br />
      <BodyLink link={"/product/ptaas/"} name={"PTaaS"} /> <br />
      <BodyLink link={"/platform/arm/"} name={"ARM"} /> <br />
      <BodyLink link={"/solutions/attack-simulation/"} name={"BAS"} /> <br />
      <BodyLink link={"/product/mast/"} name={"MAST"} /> <br />
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
      <BodyLink link={"/systems/containers/"} name={"Containers"} /> <br />
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
      <HeadLink link={"/about-us/"} name={"About Us"} /> <br />
      <BodyLink link={"/clients/"} name={"Clients"} /> <br />
      <BodyLink
        link={"/about-us/differentiators/"}
        name={"Differentiators"}
      />{" "}
      <br />
      <BodyLink link={"/about-us/values/"} name={"Values"} /> <br />
      <BodyLink link={"/about-us/reviews/"} name={"Reviews"} /> <br />
      <BodyLink link={"/resources/"} name={"Resources"} /> <br />
      <BodyLink link={"/about-us/events/"} name={"Events"} /> <br />
      <BodyLink link={"/about-us/people/"} name={"People"} /> <br />
    </LinksContainer>
    <LinksContainer className={"dib-xl"}>
      <HeadLink link={"/blog/"} name={"Blog"} /> <br />
      <HeadLink link={"/certifications/"} name={"Certifications"} /> <br />
      <HeadLink link={"/partners/"} name={"Partners"} /> <br />
      <HeadLink link={"/careers/"} name={"Careers"} /> <br />
      <HeadLink link={"/advisories/"} name={"Advisories"} /> <br />
      <HeadLink link={"/faq/"} name={"FAQ"} /> <br />
      <HeadLink
        link={"https://docs.fluidattacks.com/"}
        name={"Documentation"}
      />{" "}
      <br />
      <HeadLink link={"/contact-us/"} name={"Contact"} /> <br />
    </LinksContainer>
  </FooterMenuContainer>
);

export { LinksSection };
