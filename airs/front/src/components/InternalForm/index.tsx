import React from "react";

import { Container } from "./styledComponents";

import { IframeContainer } from "../../styles/styledComponents";
import { translate } from "../../utils/translations/translate";
import { Paragraph, Title } from "../Texts";

const InternalForm: React.FC = (): JSX.Element => {
  return (
    <Container bgColor={"#2e2e38"}>
      <Title fColor={"#f4f4f6"} fSize={"48"} marginBottom={"2"}>
        {translate.t("internalForm.title")}
      </Title>
      <Paragraph fColor={"#f4f4f6"} fSize={"24"} marginBottom={"4"}>
        {translate.t("internalForm.subTitle")}
      </Paragraph>
      <IframeContainer>
        <iframe
          sandbox={
            "allow-forms allow-top-navigation allow-same-origin allow-scripts"
          }
          src={
            "https://forms.zohopublic.com/fluidattacks1/form/Internalcontactus/formperma/A8qDPgOuvnpp21GF3c56RaPMQOZcJWMxUTYf6RTKntM"
          }
          style={{
            border: "0",
            height: "850px",
            marginBottom: "-7px",
            width: "100%",
          }}
          title={"Contact Us Form"}
        />
      </IframeContainer>
    </Container>
  );
};

export { InternalForm };
