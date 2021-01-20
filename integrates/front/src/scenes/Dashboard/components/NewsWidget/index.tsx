import AnnounceKit from "announcekit-react";
import { Glyphicon } from "react-bootstrap";
import type { IAuthContext } from "utils/auth";
import { NavItem } from "styles/styledComponents";
import React from "react";
import { authContext } from "utils/auth";

const NewsWidget: React.FC = (): JSX.Element => {
  const { userEmail }: IAuthContext = React.useContext(authContext);

  return (
    <NavItem>
      <AnnounceKit
        user={{ email: userEmail, id: userEmail }}
        widget={"https://news.fluidattacks.com/widgets/v2/ZmEGk"}
        widgetStyle={{ position: "absolute", top: "25px" }}
      >
        <Glyphicon glyph={"bullhorn"} />
      </AnnounceKit>
    </NavItem>
  );
};

export { NewsWidget };
