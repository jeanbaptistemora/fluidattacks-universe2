import React from "react";
import { Col, Label, Row } from "react-bootstrap";
import { castEventStatus, castEventType } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";

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
          <Col md={8} sm={12} xs={12}>
             <h2>{eventType}</h2>
          </Col>
          <Col md={12} sm={12} xs={12}>
             <hr/>
          </Col>
        </Row>
        <Row style={{marginBottom: "15px"}}>
          <Col md={12} sm={12} xs={12}>
            <Row>
              <Col md={2} sm={6} xs={6} className="text-right">
                {translate.t("search_findings.tab_events.id")}
              </Col>
              <Col md={2} sm={6} xs={6}>
                <Label> {props.id} </Label>
              </Col>
              <Col md={2} sm={6} xs={6} className="text-right">
                {translate.t("search_findings.tab_events.date")}
              </Col>
              <Col md={2} sm={6} xs={6}>
                <Label> {props.eventDate} </Label>
              </Col>
              <Col md={2} sm={6} xs={6} className="text-right">
                {translate.t("search_findings.tab_events.status")}
              </Col>
              <Col md={2} sm={6} xs={6}>
                <Label> {eventStatus} </Label>
              </Col>
            </Row>
          </Col>
        </Row>
      </div>
    </React.Fragment>
  );
};

export { eventHeader as EventHeader };
