import React from "react";

import { AirsLink } from "../../../../components/AirsLink";
import { Container } from "../../../../components/Container";
import type { TDisplay } from "../../../../components/Container/types";
import { Grid } from "../../../../components/Grid";
import { Text } from "../../../../components/Typography";
import { useWindowSize } from "../../../../utils/hooks/useWindowSize";
import { translate } from "../../../../utils/translations/translate";

interface IResourcesProps {
  display: TDisplay;
}

const ResourcesMenu: React.FC<IResourcesProps> = ({
  display,
}: IResourcesProps): JSX.Element => {
  const { width } = useWindowSize();

  return (
    <Container bgColor={"#ffffff"} display={display}>
      <Container
        display={width > 960 ? "flex" : "inline"}
        height={"100%"}
        justify={"center"}
        ph={3}
        scroll={"y"}
      >
        <Container maxWidth={width > 960 ? "650px" : "1440px"} mb={3} mr={4}>
          <Container ph={3}>
            <Container borderBottomColor={"#dddde3"} height={"36px"} mb={3}>
              <Text color={"#8f8fa3"} size={"xs"}>
                {translate.t("menu.resources.learn.title")}
              </Text>
            </Container>
            <Grid
              columns={width > 1200 ? 2 : 1}
              gap={"1rem"}
              ph={"0px"}
              pv={"0px"}
            >
              <Container>
                <AirsLink hoverColor={"#bf0b1a"} href={"/solutions/"}>
                  <Text color={"#2e2e38"} mb={2} size={"small"} weight={"bold"}>
                    {translate.t("menu.resources.learn.blog.title")}
                  </Text>
                </AirsLink>
                <Text color={"#535365"} mb={3} size={"xs"}>
                  {translate.t("menu.resources.learn.blog.subtitle")}
                </Text>
                <AirsLink hoverColor={"#bf0b1a"} href={"/solutions/"}>
                  <Text color={"#2e2e38"} mb={2} size={"small"} weight={"bold"}>
                    {translate.t("menu.resources.learn.downloadables.title")}
                  </Text>
                </AirsLink>
                <Text color={"#535365"} size={"xs"}>
                  {translate.t("menu.resources.learn.downloadables.subtitle")}
                </Text>
              </Container>
              <Container ph={width > 1200 ? 3 : 0}>
                <AirsLink hoverColor={"#bf0b1a"} href={"/compliance/"}>
                  <Text color={"#2e2e38"} mb={2} size={"small"} weight={"bold"}>
                    {translate.t("menu.resources.learn.clients.title")}
                  </Text>
                </AirsLink>
                <Text color={"#535365"} mb={4} size={"xs"}>
                  {translate.t("menu.resources.learn.clients.subtitle")}
                </Text>
              </Container>
            </Grid>
          </Container>
        </Container>
        <Container maxWidth={width > 960 ? "650px" : "1440px"} scroll={"y"}>
          <Container ph={3}>
            <Container borderBottomColor={"#dddde3"} pb={3}>
              <Text color={"#8f8fa3"} size={"xs"}>
                {translate.t("menu.resources.help.title")}
              </Text>
            </Container>
            <Grid columns={width > 1200 ? 2 : 1} gap={"1rem"} ph={"0px"}>
              <Container>
                <AirsLink hoverColor={"#bf0b1a"} href={"/solutions/"}>
                  <Text color={"#2e2e38"} mb={2} size={"small"} weight={"bold"}>
                    {translate.t("menu.resources.help.documentation.title")}
                  </Text>
                </AirsLink>
                <Text color={"#535365"} size={"xs"}>
                  {translate.t("menu.resources.help.documentation.subtitle")}
                </Text>
              </Container>
              <Container ph={width > 1200 ? 3 : 0}>
                <AirsLink hoverColor={"#bf0b1a"} href={"/compliance/"}>
                  <Text color={"#2e2e38"} mb={2} size={"small"} weight={"bold"}>
                    {translate.t("menu.resources.help.faq.title")}
                  </Text>
                </AirsLink>
                <Text color={"#535365"} size={"xs"}>
                  {translate.t("menu.resources.help.faq.subtitle")}
                </Text>
              </Container>
            </Grid>
          </Container>
        </Container>
      </Container>
    </Container>
  );
};

export { ResourcesMenu };
