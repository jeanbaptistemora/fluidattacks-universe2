import React from "react";
import {
  Col1,
  EventHeaderGrid,
  EventHeaderLabel,
  Label,
  Row,
} from "styles/styledComponents";
import { castEventStatus, castEventType } from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

export interface IEventHeaderProps {
  eventDate: string;
  eventStatus: string;
  eventType: string;
  id: string;
}

const eventHeader: ((props: IEventHeaderProps) => JSX.Element) =
  (props: IEventHeaderProps): JSX.Element => {
    const eventType: string = translate.t(castEventType(props.eventType));
    const eventStatus: string = translate.t(castEventStatus(props.eventStatus));

    return (
      <React.Fragment>
      <div id="events" className="tab-pane cont active">
        <Row>
          <Col1>
             <h2>{eventType}</h2>
             <hr/>
          </Col1>
        </Row>
        <Row>
          <Col1>
            <EventHeaderGrid>
              <EventHeaderLabel>
                {translate.t("search_findings.tab_events.id")}
                <Label> {props.id} </Label>
              </EventHeaderLabel>
              <EventHeaderLabel>
                {translate.t("search_findings.tab_events.date")}
                <Label> {props.eventDate} </Label>
              </EventHeaderLabel>
              <EventHeaderLabel>
                {translate.t("search_findings.tab_events.status")}
                <Label> {eventStatus} </Label>
              </EventHeaderLabel>
            </EventHeaderGrid>
          </Col1>
        </Row>
      </div>
    </React.Fragment>
  );
};

export { eventHeader as EventHeader };
