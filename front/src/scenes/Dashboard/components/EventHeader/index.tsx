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
import { castEventStatus, castEventType } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";
import { IEventDescriptionViewProps } from "../../containers/EventDescriptionView/index";

interface IEventHeaderProps {
  eventData: IEventDescriptionViewProps["eventData"];
  hasEvidence: boolean;
  isActiveTab: boolean;
  urlDescription: (() => JSX.Element);
  urlEvidence: (() => JSX.Element);
}

const eventHeader: ((props: IEventHeaderProps) => JSX.Element) =
  (props: IEventHeaderProps): JSX.Element => {
    const eventType: string = translate.t(castEventType(props.eventData.eventType));
    const eventStatus: string = translate.t(castEventStatus(props.eventData.eventStatus));

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
                <Label> {eventStatus} </Label>
              </Col>
            </Row>
          </Col>
        </Row>
        <Row style={{marginBottom: "15px"}}>
          <Col md={12} sm={12} xs={12}>
            <ul className="nav pills-tabs nav-justified">
              <li
                id="infoItem"
                className={(props.isActiveTab ? "active" : "")}
                onClick={(): void => {props.urlDescription(); }}
              >
                <a href="#info" data-toggle="tab" aria-expanded="false">
                  <i className="icon s7-note2"/>
                  &nbsp;{translate.t("search_findings.tab_events.description")}
                </a>
              </li>
              {props.hasEvidence ?
                <li
                  id="evidenceItem"
                  className={(props.isActiveTab ? "" : "active")}
                  onClick={(): void => {props.urlEvidence(); }}
                >
                  <a href="#evidence" data-toggle="tab" aria-expanded="false">
                    <i className="icon s7-note2"/>
                    &nbsp;{translate.t("search_findings.tab_events.evidence")}
                  </a>
                </li>
              : undefined}
            </ul>
          </Col>
        </Row>
      </div>
    </React.Fragment>
  );
};

export { eventHeader as EventHeader };
