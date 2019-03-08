/* tslint:disable:jsx-no-lambda jsx-no-multiline-js no-empty
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import React from "react";
import { Col, Label, Row } from "react-bootstrap";
import translate from "../../../../utils/translations/translate";

export interface IEventDescriptionViewProps {
  eventData: { eventDate?: string; eventStatus?: string; eventType?: string;  id?: string };
}

export const eventDescriptionView: React.StatelessComponent<IEventDescriptionViewProps> =
  (props: IEventDescriptionViewProps): JSX.Element => (
  <React.StrictMode>
    <div id="events" className="tab-pane cont active">
      <Row>
        <Col md={8} sm={12} xs={12}>
           <h2>{props.eventData.eventType}</h2>
        </Col>
        <Col md={12} sm={12} xs={12}>
           <hr/>
        </Col>
      </Row>
      <Row>
        <Col md={12} sm={12} xs={12}>
          <Row>
            <Col md={2} sm={6} xs={6} className="text-right">
              {translate.t("search_findings.tab_events.id")}
            </Col>
            <Col md={2} sm={6} xs={6}>
              <Label> {props.eventData.id} </Label>
            </Col>
            <Col md={2} sm={6} xs={6} className="text-right">
              {translate.t("search_findings.tab_events.date")}
            </Col>
            <Col md={2} sm={6} xs={6}>
              <Label> {props.eventData.eventDate} </Label>
            </Col>
            <Col md={2} sm={6} xs={6} className="text-right">
              {translate.t("search_findings.tab_events.status")}
            </Col>
            <Col md={2} sm={6} xs={6}>
              <Label> {props.eventData.eventStatus} </Label>
            </Col>
          </Row>
        </Col>
      </Row>
    </div>
  </React.StrictMode>
);

eventDescriptionView.defaultProps = {
  eventData:
    {
      eventDate: undefined,
      eventStatus: undefined,
      eventType: undefined,
      id: undefined,
    },
};
