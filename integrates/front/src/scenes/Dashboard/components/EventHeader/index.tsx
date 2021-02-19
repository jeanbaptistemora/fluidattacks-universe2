import React from "react";
import { translate } from "utils/translations/translate";
import {
  Col100,
  EventHeaderGrid,
  EventHeaderLabel,
  Label,
  Row,
} from "styles/styledComponents";
import { castEventStatus, castEventType } from "utils/formatHelpers";

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
    <div className={"tab-pane cont active"} id={"events"}>
      <Row>
        <Col100>
          <h2>{tEventType}</h2>
          <hr />
        </Col100>
      </Row>
      <Row>
        <Col100>
          <EventHeaderGrid>
            <EventHeaderLabel>
              {translate.t("search_findings.tab_events.id")}
              <Label> {id} </Label>
            </EventHeaderLabel>
            <EventHeaderLabel>
              {translate.t("search_findings.tab_events.date")}
              <Label> {eventDate} </Label>
            </EventHeaderLabel>
            <EventHeaderLabel>
              {translate.t("search_findings.tab_events.status")}
              <Label> {tEventStatus} </Label>
            </EventHeaderLabel>
          </EventHeaderGrid>
        </Col100>
      </Row>
    </div>
  );
};

export { EventHeader, IEventHeaderProps };
