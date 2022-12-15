import React from "react";

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
        <Container center={true} mt={3} width={"400px"}>
          <iframe
            sandbox={
              "allow-forms allow-top-navigation allow-same-origin allow-scripts"
            }
            src={
              "https://forms.zohopublic.com/fluidattacks1/form/Blogsubscribe1/formperma/0ayT6-xIcoNCI2xJJnV0KZ52IsB-UwqFkQoEKdTr3_E"
            }
            style={{
              border: "0",
              height: "225px",
              width: "100%",
            }}
            title={"Blogs Form"}
          />
        </Container>
      </Container>
    </Container>
  );
};

export { Header };
