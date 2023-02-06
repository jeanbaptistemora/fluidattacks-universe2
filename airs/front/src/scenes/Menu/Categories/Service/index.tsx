import React from "react";

import { AirsLink } from "../../../../components/AirsLink";
import { Container } from "../../../../components/Container";
import type { TDisplay } from "../../../../components/Container/types";
import { Grid } from "../../../../components/Grid";
import { Text } from "../../../../components/Typography";
import { useWindowSize } from "../../../../utils/hooks/useWindowSize";
import { translate } from "../../../../utils/translations/translate";

interface IServiceProps {
  display: TDisplay;
}

const ServiceMenu: React.FC<IServiceProps> = ({
  display,
}: IServiceProps): JSX.Element => {
  const { width } = useWindowSize();

  return (
    <Container bgColor={"#ffffff"} display={display}>
      <Container
        display={width > 960 ? "flex" : "block"}
        height={"max-content"}
        justify={"center"}
        mb={3}
      >
        <Container
          maxWidth={width > 960 ? "450px" : "1440px"}
          ph={4}
          scroll={"y"}
        >
          <Container
            borderBottomColor={"#b0b0bf"}
            height={"36px"}
            mb={3}
            pb={3}
          >
            <Text color={"#8f8fa3"}>
              {translate.t("menu.services.allInOne.title")}
            </Text>
          </Container>
          <Container ph={3}>
            <AirsLink
              hoverColor={"#bf0b1a"}
              href={"/services/continuous-hacking/"}
            >
              <Text color={"#121216"} mb={3} weight={"bold"}>
                {translate.t("menu.services.allInOne.continuous.title")}
              </Text>
            </AirsLink>
            <Text color={"#535365"} mb={3} size={"small"}>
              {translate.t("menu.services.allInOne.continuous.subtitle")}
            </Text>
          </Container>
        </Container>
        <Container maxWidth={width > 960 ? "800px" : "1440px"} ph={4}>
          <Container borderBottomColor={"#b0b0bf"} height={"36px"} pb={3}>
            <Text color={"#8f8fa3"}>
              {translate.t("menu.services.solutions.title")}
            </Text>
          </Container>
          <Grid columns={2} columnsMd={1} columnsSm={1} gap={"1rem"}>
            <Container>
              <AirsLink hoverColor={"#bf0b1a"} href={"/solutions/"}>
                <Text color={"#121216"} mb={3} weight={"bold"}>
                  {translate.t("menu.services.solutions.applicationSec.title")}
                </Text>
              </AirsLink>
              <Text color={"#535365"} size={"small"}>
                {translate.t("menu.services.solutions.applicationSec.subtitle")}
              </Text>
            </Container>
            <Container>
              <AirsLink hoverColor={"#bf0b1a"} href={"/compliance/"}>
                <Text color={"#121216"} mb={3} weight={"bold"}>
                  {translate.t("menu.services.solutions.compliance.title")}
                </Text>
              </AirsLink>
              <Text color={"#535365"} size={"small"}>
                {translate.t("menu.services.solutions.compliance.subtitle")}
              </Text>
            </Container>
          </Grid>
        </Container>
      </Container>
    </Container>
  );
};

export { ServiceMenu };
