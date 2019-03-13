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
import { default as FieldBox } from "../../components/FieldBox/index";

export interface IEventDescriptionViewProps {
  eventData: {
    accessibility: string;
    affectation: string;
    affectedComponents: string;
    analyst: string;
    client: string;
    clientProject: string;
    detail: string;
    eventDate?: string;
    eventStatus?: string;
    eventType?: string;
    id?: string;
    projectName: string;
  };
  eventEdit: (() => JSX.Element);
  eventUpdate: (() => JSX.Element);
  hasAccessibility: boolean;
  hasAffectedComponents: boolean;
  isEditable: boolean;
}

export interface IEventDescriptionHeaderProps {
  eventData: IEventDescriptionViewProps["eventData"];
  hasEvidence: boolean;
  isActiveTab: boolean;
  urlDescription: (() => JSX.Element);
  urlEvidence: (() => JSX.Element);
}

export const eventDescriptionHeader: React.StatelessComponent<IEventDescriptionHeaderProps> =
  (props: IEventDescriptionHeaderProps): JSX.Element => (
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
      <br />
      <Row>
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
  </React.StrictMode>
);

export const eventDescriptionView: React.StatelessComponent<IEventDescriptionViewProps> =
  (props: IEventDescriptionViewProps): JSX.Element => (
  <React.StrictMode>
    <div id="events" className="tab-pane cont active">
        <div className="tab-pane cont active">
        <Col md={12} sm={12} xs={12}>
          <Row>
          <Col md={6} sm={12} xs={12}>
            <FieldBox
              title={translate.t("search_findings.tab_events.description")}
              content={props.eventData.detail}
            />
            <FieldBox
              title={translate.t("search_findings.tab_events.analyst")}
              content={props.eventData.analyst}
            />
            {props.isEditable ?
                <div className="row table-row">
                  <div className="col-md-4 col-xs-12 col-sm-12">
                    <div className="table-head">
                      <label><b>{translate.t("search_findings.tab_events.affectation")}</b></label>
                    </div>
                  </div>
                  <div className="col-md-6 col-xs-12 col-sm-12">
                    <input id="affectationInput" type="text" className="form-control"/>
                  </div>
                </div>
            : <FieldBox
              title={translate.t("search_findings.tab_events.affectation")}
              content={props.eventData.affectation}
            />}
            {props.hasAffectedComponents ?
              <FieldBox
                title={translate.t("search_findings.tab_events.affected_components")}
                content={props.eventData.affectedComponents}
              />
            : undefined
            }
          </Col>
          <Col md={6} sm={12} xs={12}>
            <FieldBox
              title={translate.t("search_findings.tab_events.client")}
              content={props.eventData.client}
            />
            <FieldBox
              title={translate.t("search_findings.tab_events.client_project")}
              content={props.eventData.clientProject}
            />
            <FieldBox
              title={translate.t("search_findings.tab_events.fluid_project")}
              content={props.eventData.projectName}
            />
            {props.hasAccessibility ?
            <FieldBox
              title={translate.t("search_findings.tab_events.event_in")}
              content={props.eventData.accessibility}
            />
            : undefined
            }
          </Col>
          </Row>
        </Col>
        </div>
    </div>
  </React.StrictMode>
);

eventDescriptionView.defaultProps = {
  eventData:
    {
      accessibility: "",
      affectation: "",
      affectedComponents: "",
      analyst: "",
      client: "",
      clientProject: "",
      detail: "",
      eventDate: undefined,
      eventStatus: undefined,
      eventType: undefined,
      id: undefined,
      projectName: "",
    },
};

eventDescriptionHeader.defaultProps = {
  eventData:
    {
      accessibility: "",
      affectation: "",
      affectedComponents: "",
      analyst: "",
      client: "",
      clientProject: "",
      detail: "",
      eventDate: undefined,
      eventStatus: undefined,
      eventType: undefined,
      id: undefined,
      projectName: "",
    },
  isActiveTab: true,
};
