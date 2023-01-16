import React from "react";

import { AirsLink } from "../../../components/AirsLink";
import { Button } from "../../../components/Button";
import { Container } from "../../../components/Container";
import { Grid } from "../../../components/Grid";
import { SimpleCard } from "../../../components/SimpleCard";
import { Title } from "../../../components/Typography";
import { translate } from "../../../utils/translations/translate";

const DiscoverContinuous: React.FC = (): JSX.Element => {
  return (
    <Container
      align={"center"}
      bgColor={"#ffffff"}
      center={true}
      display={"flex"}
      justify={"center"}
      pv={5}
      wrap={"wrap"}
    >
      <Title
        color={"#bf0b1a"}
        level={3}
        mb={4}
        size={"small"}
        textAlign={"center"}
      >
        {translate.t("home.discoverContinuous.subtitle")}
      </Title>
      <Container maxWidth={"951px"} ph={4}>
        <Title
          color={"#2e2e38"}
          level={1}
          mb={4}
          size={"medium"}
          textAlign={"center"}
        >
          {translate.t("home.discoverContinuous.title")}
        </Title>
      </Container>
      <Container center={true} maxWidth={"1250px"} ph={4}>
        <Grid columns={3} columnsMd={3} columnsSm={1} gap={"1rem"}>
          <SimpleCard
            bgColor={"#f4f4f6"}
            bgGradient={"#ffffff, #f4f4f6"}
            description={translate.t("home.discoverContinuous.card1.subtitle")}
            descriptionColor={"#535365"}
            hoverColor={"#ffffff"}
            hoverShadow={true}
            image={"airs/home/DiscoverContinuous/card1.png"}
            title={translate.t("home.discoverContinuous.card1.title")}
            titleColor={"#2e2e38"}
          />
          <SimpleCard
            bgColor={"#f4f4f6"}
            bgGradient={"#ffffff, #f4f4f6"}
            description={translate.t("home.discoverContinuous.card2.subtitle")}
            descriptionColor={"#535365"}
            hoverColor={"#ffffff"}
            hoverShadow={true}
            image={"airs/home/DiscoverContinuous/card2.png"}
            title={translate.t("home.discoverContinuous.card2.title")}
            titleColor={"#2e2e38"}
          />
          <SimpleCard
            bgColor={"#f4f4f6"}
            bgGradient={"#ffffff, #f4f4f6"}
            description={translate.t("home.discoverContinuous.card3.subtitle")}
            descriptionColor={"#535365"}
            hoverColor={"#ffffff"}
            hoverShadow={true}
            image={"airs/home/DiscoverContinuous/card3.png"}
            title={translate.t("home.discoverContinuous.card3.title")}
            titleColor={"#2e2e38"}
          />
        </Grid>
      </Container>
      <Container display={"flex"} justify={"center"} maxWidth={"900px"}>
        <AirsLink href={"/services/continuous-hacking/"}>
          <Button size={"md"} variant={"primary"}>
            {translate.t("home.discoverContinuous.button")}
          </Button>
        </AirsLink>
      </Container>
    </Container>
  );
};

export { DiscoverContinuous };
