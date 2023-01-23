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
    <Container bgColor={"#ffffff"} display={width > 1200 ? display : "none"}>
      <Container display={"flex"} height={"230px"} justify={"center"}>
        <Container maxWidth={"960px"} mr={4}>
          <Container
            borderBottomColor={"#b0b0bf"}
            height={"36px"}
            mb={3}
            pb={3}
          >
            <Text color={"#8f8fa3"}>
              {translate.t("menu.company.fluid.title")}
            </Text>
          </Container>
          <Grid columns={4} gap={"1.4rem"}>
            <Container>
              <AirsLink hoverColor={"#bf0b1a"} href={"/solutions/"}>
                <Text color={"#121216"} mb={3} weight={"bold"}>
                  {translate.t("menu.company.fluid.about.title")}
                </Text>
              </AirsLink>
              <Text color={"#535365"} mb={3} size={"small"}>
                {translate.t("menu.company.fluid.about.subtitle")}
              </Text>
            </Container>
            <Container>
              <AirsLink hoverColor={"#bf0b1a"} href={"/solutions/"}>
                <Text color={"#121216"} mb={3} weight={"bold"}>
                  {translate.t("menu.company.fluid.certifications.title")}
                </Text>
              </AirsLink>
              <Text color={"#535365"} size={"small"}>
                {translate.t("menu.company.fluid.certifications.subtitle")}
              </Text>
            </Container>
            <Container>
              <AirsLink hoverColor={"#bf0b1a"} href={"/compliance/"}>
                <Text color={"#121216"} mb={3} weight={"bold"}>
                  {translate.t("menu.company.fluid.partners.title")}
                </Text>
              </AirsLink>
              <Text color={"#535365"} size={"small"}>
                {translate.t("menu.company.fluid.partners.subtitle")}
              </Text>
            </Container>
            <Container>
              <AirsLink hoverColor={"#bf0b1a"} href={"/compliance/"}>
                <Text color={"#121216"} mb={3} weight={"bold"}>
                  {translate.t("menu.company.fluid.careers.title")}
                </Text>
              </AirsLink>
              <Text color={"#535365"} mb={4} size={"small"}>
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
