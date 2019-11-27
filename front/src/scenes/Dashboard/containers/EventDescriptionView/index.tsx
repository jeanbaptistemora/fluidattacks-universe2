/* tslint:disable:jsx-no-lambda jsx-no-multiline-js no-empty
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import {
  InferableComponentEnhancer,
  lifecycle,
} from "recompose";
import { AnyAction, Reducer } from "redux";
import { formValueSelector, submit } from "redux-form";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { Button } from "../../../../components/Button/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import store from "../../../../store/index";
import { textField } from "../../../../utils/forms/fields";
import reduxWrapper from "../../../../utils/reduxWrapper";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import { EditableField } from "../../components/EditableField";
import { GenericForm } from "../../components/GenericForm/index";
import * as actions from "./actions";
import style from "./index.css";

export interface IEventDescriptionViewStateProps {
  eventData: {
    accessibility: string;
    affectation: string;
    affectedComponents: string;
    analyst: string;
    client: string;
    clientProject: string;
    detail: string;
    eventDate?: string;
    eventStatus: string;
    eventType: string;
    evidence?: string;
    id: string;
    projectName: string;
  };
  eventId: string;
  formValues: {
    editEvent: {
      values: {
        accessibility: string;
      };
    };
  };
  isActiveTab: boolean;
  isEditable: boolean;
  urlDescription: (() => JSX.Element);
  urlEvidence: (() => JSX.Element);
}

type IEventDescriptionViewBaseProps = Pick<RouteComponentProps<{ eventId: string }>, "match">;

export type IEventDescriptionViewProps = IEventDescriptionViewStateProps & IEventDescriptionViewBaseProps;

const enhance: InferableComponentEnhancer<{}> =
lifecycle<IEventDescriptionViewProps, {}>({
  componentWillUnmount(): void { store.dispatch(actions.clearEventState()); },
  componentDidMount(): void {
    mixpanel.track(
      "EventDescription",
      {
        Organization: (window as Window & { userOrganization: string }).userOrganization,
        User: (window as Window & { userName: string }).userName,
      });
    const { eventId } = this.props.match.params;
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );

    thunkDispatch(actions.loadEvent(eventId));
  },
});

const updateEvent: ((values: IEventDescriptionViewProps["eventData"]) => void) =
  (values: IEventDescriptionViewProps["eventData"]): void => {
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );
    thunkDispatch(actions.updateEvent(values));
  };

const renderEventFields: ((props: IEventDescriptionViewProps) => JSX.Element) =
  (props: IEventDescriptionViewProps): JSX.Element => {
    let hasAccessibility: boolean;
    let hasAffectedComponents: boolean;
    props.eventData.affectedComponents === "" ?
      hasAffectedComponents = false : hasAffectedComponents = true;
    props.eventData.accessibility === ""  ?
       hasAccessibility = false : hasAccessibility = true;
    const userRole: string = (window as Window & { userRole: string }).userRole;
    const isManager: boolean = _.includes(["admin", "analyst"], userRole);

    return (
      <React.Fragment>
      <Row>
      <Col md={12} sm={12} xs={12}>
      {isManager ?
      <Row className={style.rowSeparation} style={{marginBottom: "15px"}}>
        {props.eventData.eventStatus === "CLOSED" ? undefined :
        <Col md={3} mdOffset={8} sm={12} xs={12}>
          <Button
            bsStyle="primary"
            block={true}
            onClick={(): void => {
              store.dispatch(actions.editEvent());
            }}
          >
            <FluidIcon icon="edit" /> {translate.t("search_findings.tab_severity.editable")}
          </Button>
        </Col>
        }
      </Row>
      : undefined}
      <Row style={{marginBottom: "15px"}}>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            alignField="horizontalWide"
            component={textField}
            currentValue={props.eventData.detail}
            label={translate.t("search_findings.tab_events.description")}
            name="eventDescription"
            renderAsEditable={false}
            type="text"
          />
        </Col>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            alignField="horizontalWide"
            component={textField}
            currentValue={props.eventData.client}
            label={translate.t("search_findings.tab_events.client")}
            name="eventClient"
            renderAsEditable={false}
            type="text"
          />
        </Col>
      </Row>
      <Row style={{marginBottom: "15px"}}>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            alignField="horizontalWide"
            component={textField}
            currentValue={props.eventData.analyst}
            label={translate.t("search_findings.tab_events.analyst")}
            name="eventAnalyst"
            renderAsEditable={false}
            type="text"
          />
        </Col>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            alignField="horizontalWide"
            component={textField}
            currentValue={props.eventData.clientProject}
            label={translate.t("search_findings.tab_events.client_project")}
            name="eventClientProject"
            renderAsEditable={false}
            type="text"
          />
        </Col>
      </Row>
      <Row style={{marginBottom: "15px"}}>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            alignField="horizontalWide"
            component={textField}
            currentValue={props.eventData.affectation}
            label={translate.t("search_findings.tab_events.affectation")}
            name="affectation"
            renderAsEditable={props.isEditable}
            validate={[required]}
            type="text"
          />
        </Col>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            alignField="horizontalWide"
            component={textField}
            currentValue={props.eventData.projectName}
            label={translate.t("search_findings.tab_events.fluid_project")}
            name="eventFluidProject"
            renderAsEditable={false}
            type="text"
          />
        </Col>
      </Row>
      <Row style={{marginBottom: "15px"}}>
      {hasAffectedComponents ?
        <Col md={6} sm={12} xs={12}>
          <EditableField
            alignField="horizontalWide"
            component={textField}
            currentValue={props.eventData.affectedComponents}
            label={translate.t("search_findings.tab_events.affected_components")}
            name="eventAffectationComponents"
            renderAsEditable={false}
            type="text"
          />
        </Col>
      : undefined}
      {hasAccessibility ?
        <Col md={6} sm={12} xs={12}>
          <EditableField
            alignField="horizontalWide"
            component={textField}
            currentValue={props.eventData.accessibility}
            label={translate.t("search_findings.tab_events.event_in")}
            name="eventAccessibility"
            renderAsEditable={false}
            type="text"
          />
        </Col>
      : undefined}
      </Row>
      {props.isEditable ?
      <Row>
        <Col md={3} mdOffset={8} sm={12} xs={12}>
          <Button
            bsStyle="success"
            block={true}
            onClick={(): void =>  {  store.dispatch(submit("editEvent")); }}
          >
            <FluidIcon icon="loading" /> {translate.t("search_findings.tab_severity.update")}
          </Button>
        </Col>
      </Row>
      : undefined }
  </Col>
  </Row>
    </React.Fragment>
  );
};

export const descriptionComponent: React.FC<IEventDescriptionViewProps> =
  (props: IEventDescriptionViewProps): JSX.Element =>
    (
    <React.StrictMode>
      <div className={style.mainContainer} >
      <Row>
      <Col md={12} sm={12} xs={12}>
        <GenericForm
          name="editEvent"
          initialValues={{...props.eventData}}
          onSubmit={(values: IEventDescriptionViewProps["eventData"]): void => {
            updateEvent(values);
           }}
        >
          {renderEventFields(props)}
        </GenericForm>
        </Col>
      </Row>
      </div>
    </React.StrictMode>
  );

const fieldSelector: ((state: {}, ...fields: string[]) => string) = formValueSelector("editEvent");

export const eventDescriptionView: React.ComponentType<IEventDescriptionViewProps> = reduxWrapper
(
  enhance(descriptionComponent) as React.FunctionComponent<IEventDescriptionViewProps>,
  (state: StateType<Reducer>): IEventDescriptionViewProps => ({
    ...state,
    eventData: state.dashboard.eventDescription.eventData,
    formValues: {
      editEvent: {
        values: {
          affectation: fieldSelector(state, "affectation"),
        },
      },
    },
    isEditable: state.dashboard.eventDescription.isEditable,
  }),
);
