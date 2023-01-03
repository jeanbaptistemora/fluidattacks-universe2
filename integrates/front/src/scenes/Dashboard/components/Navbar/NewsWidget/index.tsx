import { faBullhorn } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import AnnounceKit from "announcekit-react";
import React, { useContext } from "react";

import { Button } from "components/Button";
import { Text } from "components/Text";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";

const NewsWidget: React.FC = (): JSX.Element => {
  const { userEmail }: IAuthContext = useContext(authContext);

  return (
    <Button size={"sm"}>
      <AnnounceKit
        user={{ email: userEmail, id: userEmail }}
        widget={"https://news.fluidattacks.tech/widgets/v2/ZmEGk"}
        widgetStyle={{ left: "24px", position: "absolute", top: "6px" }}
      >
        <Text size={"medium"}>
          <FontAwesomeIcon icon={faBullhorn} />
        </Text>
      </AnnounceKit>
    </Button>
  );
};

export { NewsWidget };
