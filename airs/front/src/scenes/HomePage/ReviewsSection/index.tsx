import React from "react";
import { BsArrowRight } from "react-icons/bs";

import { CardFooter } from "./styledComponents";

import { AirsLink } from "../../../components/AirsLink";
import { CloudImage } from "../../../components/CloudImage";
import { Container } from "../../../components/Container";
import { Text, Title } from "../../../components/Typography";
import { translate } from "../../../utils/translations/translate";

const Reviews: React.FC = (): JSX.Element => {
  return (
    <Container
      align={"center"}
      bgColor={"#ffffff"}
      display={"flex"}
      justify={"center"}
      minHeight={"500px"}
      wrap={"wrap"}
    >
      <Container maxWidth={"600px"} minWidth={"300px"} mt={5} ph={4} phMd={4}>
        <Title color={"#2e2e38"} level={1} mb={1} size={"medium"}>
          {translate.t("home.reviews.title")}
        </Title>
        <Text color={"#535365"} mb={4} mt={4} size={"big"}>
          {translate.t("home.reviews.subtitle")}
        </Text>
        <Container display={"flex"} wrap={"wrap"}>
          <AirsLink
            decoration={"underline"}
            hoverColor={"#bf0b1a"}
            href={"https://clutch.co/profile/fluid-attacks"}
          >
            <Text color={"#2e2e38"} mr={1} mt={3} size={"big"} weight={"bold"}>
              {"Public reviews"}
            </Text>
          </AirsLink>
          <CloudImage
            alt={"reviews image"}
            src={"airs/home/SuccessReviews/reviews.png"}
            styles={"mv2 mh2 w4"}
          />
        </Container>
      </Container>
      <Container
        align={"center"}
        display={"flex"}
        justify={"center"}
        maxWidth={"700px"}
        wrap={"wrap"}
      >
        <Container
          align={"start"}
          bgGradient={"#ffffff, #f4f4f6"}
          borderColor={"#dddde3"}
          borderHoverColor={"#bf0b1a"}
          br={2}
          direction={"column"}
          display={"flex"}
          height={"360px"}
          hoverColor={"#ffe5e7"}
          maxWidth={"280px"}
          mh={3}
          minWidth={"280px"}
          mv={4}
          ph={3}
          pv={3}
        >
          <Title color={"#bf0b1a"} level={4} mt={4} size={"xxs"}>
            {"SUCCESS STORY"}
          </Title>
          <CloudImage
            alt={"success story 1"}
            src={"airs/home/SuccessReviews/logo-payvalida.png"}
            styles={"mv3 w-50"}
          />
          <Text color={"#535365"} size={"medium"}>
            {translate.t("home.reviews.successStory.description1")}
          </Text>
          <CardFooter>
            <Container align={"center"} display={"flex"} pb={2} wrap={"wrap"}>
              <AirsLink
                decoration={"underline"}
                hoverColor={"#bf0b1a"}
                href={"https://fluidattacks.docsend.com/view/u37w4yqbh27e5dte"}
              >
                <Text color={"#2e2e38"} mr={1} size={"small"} weight={"bold"}>
                  {"Read success story"}
                </Text>
              </AirsLink>
              <BsArrowRight size={10} />
            </Container>
          </CardFooter>
        </Container>
        <Container
          align={"start"}
          bgGradient={"#ffffff, #f4f4f6"}
          borderColor={"#dddde3"}
          borderHoverColor={"#bf0b1a"}
          br={2}
          direction={"column"}
          display={"flex"}
          height={"360px"}
          hoverColor={"#ffe5e7"}
          maxWidth={"280px"}
          minWidth={"280px"}
          mv={4}
          ph={3}
          pv={3}
        >
          <Title color={"#bf0b1a"} level={4} mt={4} size={"xxs"}>
            {"SUCCESS STORY"}
          </Title>
          <CloudImage
            alt={"success story 2"}
            src={"airs/home/SuccessReviews/logo_proteccion.png"}
            styles={"mv3 w-50"}
          />
          <Text color={"#535365"} size={"medium"}>
            {translate.t("home.reviews.successStory.description2")}
          </Text>
          <CardFooter>
            <Container align={"center"} display={"flex"} pb={2} wrap={"wrap"}>
              <AirsLink
                decoration={"underline"}
                hoverColor={"#bf0b1a"}
                href={"https://fluidattacks.docsend.com/view/v3aj7p3sixmh6ict"}
              >
                <Text color={"#2e2e38"} mr={1} size={"small"} weight={"bold"}>
                  {"Read success story"}
                </Text>
              </AirsLink>
              <BsArrowRight size={10} />
            </Container>
          </CardFooter>
        </Container>
      </Container>
    </Container>
  );
};

export { Reviews };
