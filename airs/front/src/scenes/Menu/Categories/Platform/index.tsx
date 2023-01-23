import React from "react";

import { AirsLink } from "../../../../components/AirsLink";
import { Container } from "../../../../components/Container";
import type { TDisplay } from "../../../../components/Container/types";
import { Grid } from "../../../../components/Grid";
import { Text } from "../../../../components/Typography";
import { useWindowSize } from "../../../../utils/hooks/useWindowSize";
import { translate } from "../../../../utils/translations/translate";

interface IPlatformProps {
  display: TDisplay;
}

const PlatformMenu: React.FC<IPlatformProps> = ({
  display,
}: IPlatformProps): JSX.Element => {
  const { width } = useWindowSize();

  return (
    <Container bgColor={"#ffffff"} display={width > 1200 ? display : "none"}>
      <Container display={"flex"} height={"380px"} justify={"center"}>
        <Container maxWidth={"350px"} mr={4}>
          <Container
            borderBottomColor={"#b0b0bf"}
            height={"36px"}
            mb={3}
            mt={3}
            pb={3}
          >
            <Text color={"#8f8fa3"}>
              {translate.t("menu.platform.aSinglePane.title")}
            </Text>
          </Container>
          <AirsLink hoverColor={"#bf0b1a"} href={"/platform/"}>
            <Text color={"#121216"} mb={3} weight={"bold"}>
              {translate.t("menu.platform.aSinglePane.platformOverview.title")}
            </Text>
          </AirsLink>
          <Text color={"#535365"} mb={3} size={"small"}>
            {translate.t("menu.platform.aSinglePane.platformOverview.subtitle")}
          </Text>
          <AirsLink hoverColor={"#bf0b1a"} href={"/platform/"}>
            <Text color={"#121216"} mb={3} mt={2} weight={"bold"}>
              {translate.t("menu.platform.aSinglePane.ARMplatform.title")}
            </Text>
          </AirsLink>
          <Text color={"#535365"} size={"small"}>
            {translate.t("menu.platform.aSinglePane.ARMplatform.subtitle")}
          </Text>
        </Container>
        <Container maxWidth={"768px"}>
          <Container
            borderBottomColor={"#b0b0bf"}
            height={"36px"}
            mt={3}
            pb={3}
          >
            <Text color={"#8f8fa3"}>
              {translate.t("menu.platform.products.title")}
            </Text>
          </Container>
          <Grid columns={2} gap={"1rem"}>
            <Container width={"370px"}>
              <AirsLink hoverColor={"#bf0b1a"} href={"/solutions/"}>
                <Text color={"#121216"} mb={3} weight={"bold"}>
                  {translate.t("menu.platform.products.links.sast")}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#bf0b1a"} href={"/solutions/"}>
                <Text color={"#121216"} mb={3} weight={"bold"}>
                  {translate.t("menu.platform.products.links.dast")}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#bf0b1a"} href={"/solutions/"}>
                <Text color={"#121216"} mb={3} weight={"bold"}>
                  {translate.t("menu.platform.products.links.sca")}
                </Text>
              </AirsLink>
            </Container>
            <Container>
              <AirsLink hoverColor={"#bf0b1a"} href={"/compliance/"}>
                <Text color={"#121216"} mb={3} weight={"bold"}>
                  {translate.t("menu.platform.products.links.re")}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#bf0b1a"} href={"/compliance/"}>
                <Text color={"#121216"} mb={3} weight={"bold"}>
                  {translate.t("menu.platform.products.links.ptaas")}
                </Text>
              </AirsLink>
              <AirsLink hoverColor={"#bf0b1a"} href={"/compliance/"}>
                <Text color={"#121216"} mb={3} weight={"bold"}>
                  {translate.t("menu.platform.products.links.mast")}
                </Text>
              </AirsLink>
            </Container>
          </Grid>
        </Container>
      </Container>
    </Container>
  );
};

export { PlatformMenu };
