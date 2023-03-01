/* eslint react/forbid-component-props: 0 */
import dayjs from "dayjs";
import React from "react";
import {
  FaFacebookSquare,
  FaInstagramSquare,
  FaLinkedin,
  FaTwitterSquare,
  FaYoutubeSquare,
} from "react-icons/fa";

import { AirsLink } from "../../../components/AirsLink";
import { CloudImage } from "../../../components/CloudImage";
import { Container } from "../../../components/Container";
import { Text } from "../../../components/Typography";
import { translate } from "../../../utils/translations/translate";

const DesktopFooter: React.FC = (): JSX.Element => {
  const currentYear = dayjs().year();

  return (
    <Container align={"end"}>
      <Container
        bgColor={"#121216"}
        display={"flex"}
        justify={"center"}
        minHeight={"200px"}
        pv={5}
        wrap={"wrap"}
      >
        <Container display={"flex"} maxWidth={"1440px"} wrap={"wrap"}>
          <Container maxWidth={"470px"} ph={3} width={"30%"}>
            <Container width={"223px"}>
              <AirsLink href={"/"}>
                <CloudImage
                  alt={"Fluid Logo Footer"}
                  src={"logo-fluid-dark-2022"}
                />
              </AirsLink>
            </Container>
            <Container maxWidth={"465px"}>
              <Text color={"#8f8fa3"} mb={2} size={"big"} weight={"bold"}>
                {translate.t("footer.title")}
              </Text>
              <Text color={"#8f8fa3"} size={"medium"}>
                {translate.t("footer.subtitle")}
              </Text>
            </Container>
            <Container pv={4}>
              <AirsLink
                hoverColor={"#b0b0bf"}
                href={"https://www.linkedin.com/company/fluidattacks/"}
              >
                <FaLinkedin
                  size={28}
                  style={{ color: "#ffffff", marginRight: "16px" }}
                />
              </AirsLink>
              <AirsLink
                href={"https://www.facebook.com/Fluid-Attacks-267692397253577/"}
              >
                <FaFacebookSquare
                  size={28}
                  style={{ color: "#ffffff", marginRight: "16px" }}
                />
              </AirsLink>
              <AirsLink href={"https://twitter.com/fluidattacks/"}>
                <FaTwitterSquare
                  size={28}
                  style={{ color: "#ffffff", marginRight: "16px" }}
                />
              </AirsLink>
              <AirsLink href={"https://www.youtube.com/c/fluidattacks/"}>
                <FaYoutubeSquare
                  size={28}
                  style={{ color: "#ffffff", marginRight: "16px" }}
                />
              </AirsLink>
              <AirsLink href={"https://www.instagram.com/fluidattacks/"}>
                <FaInstagramSquare size={27} style={{ color: "#ffffff" }} />
              </AirsLink>
            </Container>
          </Container>
          <Container display={"flex"} ph={2} width={"65%"} wrap={"wrap"}>
            <Container height={"100%"} width={"25%"}>
              <Text
                color={"#8f8fa3"}
                mb={2}
                mt={2}
                size={"medium"}
                weight={"bold"}
              >
                {"SERVICE"}
              </Text>
              <AirsLink
                hoverColor={"#b0b0bf"}
                href={"/services/continuous-hacking/"}
              >
                <Text color={"#ffffff"} mb={4} size={"small"}>
                  {translate.t("menu.services.allInOne.continuous.title")}
                </Text>
              </AirsLink>
              <Text
                color={"#8f8fa3"}
                mb={2}
                mt={3}
                size={"medium"}
                weight={"bold"}
              >
                {"SOLUTIONS"}
              </Text>
              <AirsLink hoverColor={"#b0b0bf"} href={"/solutions/"}>
                <Text color={"#ffffff"} mb={2} size={"small"}>
                  {translate.t("menu.services.solutions.applicationSec.title")}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/compliance/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {translate.t("menu.services.solutions.compliance.title")}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/systems/"}>
                <Text color={"#ffffff"} mt={4} size={"small"} weight={"bold"}>
                  {"Systems"}
                </Text>
              </AirsLink>
            </Container>
            <Container pl={4} width={"25%"}>
              <Text
                color={"#8f8fa3"}
                mb={2}
                mt={2}
                size={"medium"}
                weight={"bold"}
              >
                {"PLATFORM"}
              </Text>
              <AirsLink hoverColor={"#b0b0bf"} href={"/platform/"}>
                <Text color={"#ffffff"} mb={4} size={"small"}>
                  {translate.t(
                    "menu.platform.aSinglePane.platformOverview.title"
                  )}
                </Text>
              </AirsLink>
              <Text
                color={"#8f8fa3"}
                mb={2}
                mt={2}
                size={"medium"}
                weight={"bold"}
              >
                {"SCANNING AND ANALYSIS  PRODUCTS"}
              </Text>
              <AirsLink hoverColor={"#b0b0bf"} href={"/product/sast/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"SAST"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/product/dast/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"DAST"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/product/mast/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"MAST"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/product/sca/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"SCA"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/platform/arm/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {translate.t("menu.platform.aSinglePane.ARMplatform.title")}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/product/ptaas/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"PTaaS"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/product/re/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"RE"}
                </Text>
              </AirsLink>
            </Container>
            <Container pl={5} width={"25%"}>
              <Text
                color={"#8f8fa3"}
                mb={2}
                mt={2}
                size={"medium"}
                weight={"bold"}
              >
                {"RESOURCES"}
              </Text>
              <AirsLink hoverColor={"#b0b0bf"} href={"/blog/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Blog"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/clients/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Clients"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/resources/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Downloadables"}
                </Text>
              </AirsLink>
              <AirsLink
                decoration={"none"}
                hoverColor={"#b0b0bf"}
                href={"https://docs.fluidattacks.com/"}
              >
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Documentation"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/faq/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"FAQs"}
                </Text>
              </AirsLink>
            </Container>
            <Container pl={5} width={"25%"}>
              <Text
                color={"#8f8fa3"}
                mb={2}
                mt={2}
                size={"medium"}
                weight={"bold"}
              >
                {"COMPANY"}
              </Text>
              <AirsLink hoverColor={"#b0b0bf"} href={"/about-us/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"About us"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/certifications/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Certifications"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/partners/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Partners"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/careers/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Careers"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/contact-us/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Contact us"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/plans/"}>
                <Text color={"#ffffff"} mt={4} size={"small"} weight={"bold"}>
                  {"Plans"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/advisories/"}>
                <Text color={"#ffffff"} mt={4} size={"small"} weight={"bold"}>
                  {"Advisories"}
                </Text>
              </AirsLink>
            </Container>
          </Container>
        </Container>
      </Container>
      <Container
        align={"center"}
        bgColor={"#25252d"}
        display={"flex"}
        height={"80px"}
        justify={"center"}
      >
        <Container
          display={"flex"}
          height={"20px"}
          justify={"center"}
          width={"50%"}
        >
          <Text color={"#b0b0bf"} size={"xs"} textAlign={"center"}>
            {`Copyright © ${currentYear} Fluid Attacks. We hack your software. All rights reserved.`}
          </Text>
        </Container>
        <Container
          display={"flex"}
          height={"25px"}
          justify={"center"}
          width={"50%"}
        >
          <AirsLink
            hoverColor={"#b0b0bf"}
            href={"https://status.fluidattacks.com/"}
          >
            <Text color={"#ffffff"} mr={2} size={"xs"}>
              {"Service status"}
            </Text>
          </AirsLink>
          <AirsLink
            decoration={"underline"}
            hoverColor={"#b0b0bf"}
            href={"/terms-use/"}
          >
            <Text color={"#ffffff"} mr={2} size={"xs"}>
              {"Terms of use"}
            </Text>
          </AirsLink>
          <AirsLink
            decoration={"underline"}
            hoverColor={"#b0b0bf"}
            href={"/privacy/"}
          >
            <Text color={"#ffffff"} mr={2} size={"xs"}>
              {"Privacy policy"}
            </Text>
          </AirsLink>
          <AirsLink
            decoration={"underline"}
            hoverColor={"#b0b0bf"}
            href={"/cookie/"}
          >
            <Text color={"#ffffff"} mr={2} size={"xs"}>
              {"Cookie policy"}
            </Text>
          </AirsLink>
        </Container>
      </Container>
    </Container>
  );
};

export { DesktopFooter };
