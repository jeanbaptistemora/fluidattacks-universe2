import AnnounceKit from "announcekit-react";
import { Glyphicon } from "react-bootstrap";
import { NavItem } from "styles/styledComponents";
import React from "react";

const NewsWidget: React.FC = (): JSX.Element => {
  const { userEmail } = window as typeof window & { userEmail: string };

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
