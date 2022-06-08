import { faBullhorn } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import AnnounceKit from "announcekit-react";
import React, { useContext } from "react";

import { ButtonOpacity } from "components/Button";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";

const NewsWidget: React.FC = (): JSX.Element => {
  const { userEmail }: IAuthContext = useContext(authContext);

  return (
    <ButtonOpacity>
      <AnnounceKit
        user={{ email: userEmail, id: userEmail }}
        widget={"https://news.fluidattacks.com/widgets/v2/ZmEGk"}
        widgetStyle={{ position: "absolute", top: "25px" }}
      >
        <FontAwesomeIcon color={"#2e2e38"} icon={faBullhorn} />
      </AnnounceKit>
    </ButtonOpacity>
  );
};

export { NewsWidget };
