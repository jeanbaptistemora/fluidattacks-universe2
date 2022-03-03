import React from "react";

import { HeaderContainer } from "./styles";

import { Badge } from "components/Badge";
import {
  Col100,
  EventHeaderGrid,
  EventHeaderLabel,
  Row,
} from "styles/styledComponents";
import { castEventStatus, castEventType } from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

interface IEventHeaderProps {
  eventDate: string;
  eventStatus: string;
  eventType: string;
  id: string;
}

const EventHeader: (props: IEventHeaderProps) => JSX.Element = (
  props: IEventHeaderProps
): JSX.Element => {
  const { eventDate, eventStatus, eventType, id } = props;
  const tEventType: string = translate.t(castEventType(eventType));
  const tEventStatus: string = translate.t(castEventStatus(eventStatus));

  return (
    <HeaderContainer>
      <Row>
        <Col100>
          <h2>{tEventType}</h2>
        </Col100>
      </Row>
      <Row>
        <Col100>
          <EventHeaderGrid>
            <EventHeaderLabel>
              {translate.t("searchFindings.tabEvents.id")}
              &nbsp;<Badge variant={"gray"}>{id}</Badge>
            </EventHeaderLabel>
            <EventHeaderLabel>
              {translate.t("searchFindings.tabEvents.date")}
              &nbsp;<Badge variant={"gray"}>{eventDate}</Badge>
            </EventHeaderLabel>
            <EventHeaderLabel>
              {translate.t("searchFindings.tabEvents.status")}
              &nbsp;<Badge variant={"gray"}>{tEventStatus}</Badge>
            </EventHeaderLabel>
          </EventHeaderGrid>
        </Col100>
      </Row>
    </HeaderContainer>
  );
};

export { EventHeader, IEventHeaderProps };
