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

const MobileFooter: React.FC = (): JSX.Element => {
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
          <Container display={"flex"} justify={"center"}>
            <Container
              borderBottomColor={"#8f8fa3"}
              display={"flex"}
              maxWidth={"760px"}
              pb={4}
              ph={4}
              wrap={"wrap"}
            >
              <Container height={"max-content"} width={"50%"}>
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
                    {translate.t(
                      "menu.services.solutions.applicationSec.title"
                    )}
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
              <Container pl={3} width={"50%"}>
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
          <Container>
            <Container display={"flex"} mb={3} ph={3} pt={4} wrap={"wrap"}>
              <Container maxWidth={"223px"} width={"40%"}>
                <CloudImage
                  alt={"Fluid Logo Footer"}
                  src={"logo-fluid-dark-2022"}
                />
              </Container>
              <Container
                display={"flex"}
                justify={"end"}
                maxWidth={"600px"}
                pv={4}
                width={"60%"}
              >
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
            <Container ph={4}>
              <Text color={"#8f8fa3"} mb={4} size={"big"} weight={"bold"}>
                {translate.t("footer.title")}
              </Text>
              <Text color={"#8f8fa3"} size={"medium"}>
                {translate.t("footer.subtitle")}
              </Text>
            </Container>
          </Container>
        </Container>
      </Container>
      <Container
        align={"center"}
        bgColor={"#25252d"}
        display={"flex"}
        height={"130px"}
        justify={"center"}
        wrap={"wrap"}
      >
        <Container
          display={"flex"}
          height={"30px"}
          justify={"center"}
          width={"100%"}
        >
          <Text color={"#b0b0bf"} size={"xs"} textAlign={"center"}>
            {
              "Copyright © 2022 Fluid Attacks. We hack your software. All rights reserved."
            }
          </Text>
        </Container>
        <Container
          display={"flex"}
          height={"15px"}
          justify={"center"}
          width={"100%"}
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
        </Container>
        <Container
          display={"flex"}
          height={"15px"}
          justify={"center"}
          width={"100%"}
        >
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

export { MobileFooter };