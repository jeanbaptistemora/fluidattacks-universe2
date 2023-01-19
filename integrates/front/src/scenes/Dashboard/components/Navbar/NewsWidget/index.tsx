import { faBullhorn } from "@fortawesome/free-solid-svg-icons";
import AnnounceKit from "announcekit-react";
import React, { useContext } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Container } from "components/Container";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";

const NewsWidget: React.FC = (): JSX.Element => {
  const { userEmail }: IAuthContext = useContext(authContext);
  const { t } = useTranslation();

  return (
    <Container position={"relative"}>
      <AnnounceKit
        user={{ email: userEmail, id: userEmail }}
        widget={"https://news.fluidattacks.tech/widgets/v2/ZmEGk"}
        widgetStyle={{
          left: "85%",
          position: "absolute",
          top: "25%",
        }}
      >
        <Button icon={faBullhorn} size={"md"}>
          {t("components.navBar.news")}
        </Button>
      </AnnounceKit>
    </Container>
  );
};

export { NewsWidget };
