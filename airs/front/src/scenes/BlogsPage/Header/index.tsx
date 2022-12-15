import React from "react";

import { AirsLink } from "../../../components/AirsLink";
import { Button } from "../../../components/Button";
import { Container } from "../../../components/Container";
import { Text, Title } from "../../../components/Typography";
import { translate } from "../../../utils/translations/translate";

const Header: React.FC = (): JSX.Element => {
  return (
    <Container bgColor={"#2e2e38"} ph={4} pv={5}>
      <Container center={true} maxWidth={"1200px"}>
        <Title
          color={"#fff"}
          level={1}
          mb={3}
          size={"big"}
          sizeSm={"medium"}
          textAlign={"center"}
        >
          {translate.t("blog.title")}
        </Title>
        <Text color={"#dddde3"} size={"big"} textAlign={"center"}>
          {translate.t("blog.description")}
        </Text>
        <Container display={"flex"} justify={"center"} mt={3} wrap={"wrap"}>
          <Container width={"auto"} widthSm={"100%"}>
            <AirsLink href={"/subscription/"}>
              <Button display={"block"} variant={"primary"}>
                {"Subscribe to our blog"}
              </Button>
            </AirsLink>
          </Container>
        </Container>
      </Container>
    </Container>
  );
};

export { Header };
