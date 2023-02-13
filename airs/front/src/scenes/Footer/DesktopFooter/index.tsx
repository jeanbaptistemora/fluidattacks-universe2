/* eslint react/forbid-component-props: 0 */
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
              <CloudImage
                alt={"Fluid Logo Footer"}
                src={"logo-fluid-dark-2022"}
              />
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
              <FaLinkedin
                size={28}
                style={{ color: "#ffffff", marginRight: "16px" }}
              />
              <FaFacebookSquare
                size={28}
                style={{ color: "#ffffff", marginRight: "16px" }}
              />
              <FaTwitterSquare
                size={28}
                style={{ color: "#ffffff", marginRight: "16px" }}
              />
              <FaYoutubeSquare
                size={28}
                style={{ color: "#ffffff", marginRight: "16px" }}
              />
              <FaInstagramSquare size={27} style={{ color: "#ffffff" }} />
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
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
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
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={2} size={"small"}>
                  {translate.t("menu.services.solutions.applicationSec.title")}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {translate.t("menu.services.solutions.compliance.title")}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
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
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={2} size={"small"}>
                  {translate.t(
                    "menu.platform.aSinglePane.platformOverview.title"
                  )}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={4} size={"small"}>
                  {translate.t("menu.platform.aSinglePane.ARMplatform.title")}
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
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"SAST"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"DAST"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"SCA"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"RE"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"PTaaS"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"MAST"}
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
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Blog"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Clients"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Downloadables"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Documentation"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
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
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"About us"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Certifications"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Partners"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Careers"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"Contact us"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
                <Text color={"#ffffff"} mt={4} size={"small"} weight={"bold"}>
                  {"Plans"}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#b0b0bf"} href={"/"}>
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
            {
              "Copyright © 2022 Fluid Attacks. We hack your software. All rights reserved."
            }
          </Text>
        </Container>
        <Container
          display={"flex"}
          height={"20px"}
          justify={"center"}
          width={"50%"}
        >
          <AirsLink decoration={"underline"} hoverColor={"#b0b0bf"} href={"/"}>
            <Text color={"#ffffff"} mr={2} size={"xs"}>
              {"Service status"}
            </Text>
          </AirsLink>
          <AirsLink decoration={"underline"} hoverColor={"#b0b0bf"} href={"/"}>
            <Text color={"#ffffff"} mr={2} size={"xs"}>
              {"Terms of use"}
            </Text>
          </AirsLink>
          <AirsLink decoration={"underline"} hoverColor={"#b0b0bf"} href={"/"}>
            <Text color={"#ffffff"} mr={2} size={"xs"}>
              {"Privacy policy"}
            </Text>
          </AirsLink>
          <AirsLink decoration={"underline"} hoverColor={"#b0b0bf"} href={"/"}>
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
