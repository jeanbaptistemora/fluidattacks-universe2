import React from "react";

import { AirsLink } from "../../../../components/AirsLink";
import { Container } from "../../../../components/Container";
import type { TDisplay } from "../../../../components/Container/types";
import { Grid } from "../../../../components/Grid";
import { Text } from "../../../../components/Typography";
import { useWindowSize } from "../../../../utils/hooks/useWindowSize";
import { translate } from "../../../../utils/translations/translate";

interface ICompanyProps {
  display: TDisplay;
}

const CompanyMenu: React.FC<ICompanyProps> = ({
  display,
}: ICompanyProps): JSX.Element => {
  const { width } = useWindowSize();

  return (
    <Container
      bgColor={"#ffffff"}
      display={display}
      shadowBottom={width > 1240}
    >
      <Container
        display={"flex"}
        height={"max-content"}
        justify={"center"}
        pb={3}
        ph={4}
      >
        <Container maxWidth={width > 1200 ? "1218px" : "100%"}>
          <Container
            borderBottomColor={"#dddde3"}
            height={"36px"}
            mb={3}
            pb={3}
          >
            <Text color={"#8f8fa3"} size={"xs"}>
              {translate.t("menu.company.fluid.title")}
            </Text>
          </Container>
          <Grid
            columns={width > 1200 ? 4 : 2}
            columnsMd={1}
            gap={width > 1200 ? "4rem" : "1.25rem"}
            ph={"0px"}
            pv={"0px"}
          >
            <Container>
              <AirsLink hoverColor={"#bf0b1a"} href={"/solutions/"}>
                <Text color={"#2e2e38"} mb={2} size={"small"} weight={"bold"}>
                  {translate.t("menu.company.fluid.about.title")}
                </Text>
              </AirsLink>
              <Text color={"#535365"} size={"xs"}>
                {translate.t("menu.company.fluid.about.subtitle")}
              </Text>
            </Container>
            <Container>
              <AirsLink hoverColor={"#bf0b1a"} href={"/solutions/"}>
                <Text color={"#2e2e38"} mb={2} size={"small"} weight={"bold"}>
                  {translate.t("menu.company.fluid.certifications.title")}
                </Text>
              </AirsLink>
              <Text color={"#535365"} size={"xs"}>
                {translate.t("menu.company.fluid.certifications.subtitle")}
              </Text>
            </Container>
            <Container>
              <AirsLink hoverColor={"#bf0b1a"} href={"/compliance/"}>
                <Text color={"#2e2e38"} mb={2} size={"small"} weight={"bold"}>
                  {translate.t("menu.company.fluid.partners.title")}
                </Text>
              </AirsLink>
              <Text color={"#535365"} size={"xs"}>
                {translate.t("menu.company.fluid.partners.subtitle")}
              </Text>
            </Container>
            <Container>
              <AirsLink hoverColor={"#bf0b1a"} href={"/compliance/"}>
                <Text color={"#2e2e38"} mb={2} size={"small"} weight={"bold"}>
                  {translate.t("menu.company.fluid.careers.title")}
                </Text>
              </AirsLink>
              <Text color={"#535365"} mb={4} size={"xs"}>
                {translate.t("menu.company.fluid.careers.subtitle")}
              </Text>
            </Container>
          </Grid>
        </Container>
      </Container>
    </Container>
  );
};

export { CompanyMenu };
