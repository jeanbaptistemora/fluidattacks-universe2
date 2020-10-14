import React from "react";
import {
  Col100,
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
          <Col100>
             <h2>{eventType}</h2>
             <hr/>
          </Col100>
        </Row>
        <Row>
          <Col100>
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
          </Col100>
        </Row>
      </div>
    </React.Fragment>
  );
};

export { eventHeader as EventHeader };
