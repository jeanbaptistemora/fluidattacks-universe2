/* tslint:disable jsx-no-lambda number-literal-format jsx-no-multiline-js
 * JSX-NO-LAMBDA: Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 *
 * JSX-NO-MULTILINE-JS: necessary for the sake of readability of the code that dynamically renders fields
 * as input or <p> depending on their state
 */

import React from "react";
import { Button, Col, Glyphicon, Row } from "react-bootstrap";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { AnyAction, Reducer } from "redux";
import { formValueSelector, submit } from "redux-form";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import store from "../../../../store/index";
import { castFields } from "../../../../utils/formatHelpers";
import { dropdownField } from "../../../../utils/forms/fields";
import reduxWrapper from "../../../../utils/reduxWrapper";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import { EditableField } from "../../components/EditableField";
import { GenericForm } from "../../components/GenericForm/index";
import * as actions from "./actions";
import style from "./index.css";

export interface ISeverityViewProps {
  canEdit: boolean;
  criticity: number;
  cvssVersion: string;
  dataset: {
    accessComplexity: string;
    accessVector: string;
    attackComplexity: string;
    attackVector: string;
    authentication: string;
    availabilityImpact: string;
    availabilityRequirement: string;
    collateralDamagePotential: string;
    confidenceLevel: string;
    confidentialityImpact: string;
    confidentialityRequirement: string;
    exploitability: string;
    findingDistribution: string;
    integrityImpact: string;
    integrityRequirement: string;
    modifiedAttackComplexity: string;
    modifiedAttackVector: string;
    modifiedAvailabilityImpact: string;
    modifiedConfidentialityImpact: string;
    modifiedIntegrityImpact: string;
    modifiedPrivilegesRequired: string;
    modifiedSeverityScope: string;
    modifiedUserInteraction: string;
    privilegesRequired: string;
    remediationLevel: string;
    reportConfidence: string;
    resolutionLevel: string;
    severityScope: string;
    userInteraction: string;
  };
  findingId: string;
  formValues: { editSeverity: { values: { cvssVersion: string } } };
  isEditing: boolean;
}

export interface ISeverityField {
  currentValue: string;
  name: string;
  options: {[value: string]: string};
  title: string;
}

const enhance: InferableComponentEnhancer<{}> =
lifecycle({
  componentDidMount(): void {
    const { findingId } = this.props as ISeverityViewProps;
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );

    thunkDispatch(actions.loadSeverity(findingId));
  },
});

const renderEditPanel: ((arg1: ISeverityViewProps) => JSX.Element) = (props: ISeverityViewProps): JSX.Element => (
  <Row>
    <Row>
      <Col md={2} mdOffset={10} xs={12} sm={12}>
        <Button bsStyle="primary" block={true} onClick={(): void => { store.dispatch(actions.editSeverity()); }}>
          <Glyphicon glyph="edit" /> {translate.t("search_findings.tab_severity.editable")}
        </Button>
      </Col>
    </Row>
    <br />
    {props.isEditing
      ?
      <Row>
        <Col md={2} mdOffset={10} xs={12} sm={12}>
          <Button bsStyle="success" block={true} type="submit" onClick={(): void => { submit("editSeverity"); }}>
            <Glyphicon glyph="repeat" /> {translate.t("search_findings.tab_severity.update")}
          </Button>
        </Col>
      </Row>
      : undefined
    }
  </Row>
);

const renderCVSSFields: ((props: ISeverityViewProps, cvssVersion: ISeverityViewProps["cvssVersion"]) => JSX.Element[]) =
  (props: ISeverityViewProps, cvssVersion: ISeverityViewProps["cvssVersion"]): JSX.Element[] =>
  castFields(props.dataset, cvssVersion)
        .map((field: ISeverityField, index: number) => {
        const value: string = field.currentValue;
        const text: string = field.options[value];

        return (
          <Row className={style.row} key={index}>
            <EditableField
              alignField="horizontal"
              component={dropdownField}
              currentValue={`${value} | ${translate.t(text)}`}
              label={field.title}
              name={field.name}
              renderAsEditable={props.isEditing}
              validate={[required]}
            >
              <option value="" selected={true} />
              {Object.keys(field.options)
                .map((key: string) => (
                <option value={`${key}`}>
                  {translate.t(field.options[key])}
                </option>
              ))}
            </EditableField>
          </Row>
        );
      });

const renderSeverityFields: ((props: ISeverityViewProps) => JSX.Element) = (props: ISeverityViewProps): JSX.Element => {
  const cvssVersion: string = (props.isEditing)
    ? props.formValues.editSeverity.values.cvssVersion
    : props.cvssVersion;

  return (
    <React.Fragment>
      {props.canEdit ? renderEditPanel(props) : undefined}
      <Row className={style.row}>
        <EditableField
          alignField="horizontal"
          component={dropdownField}
          currentValue={props.cvssVersion}
          label={translate.t("search_findings.tab_severity.cvss_version")}
          name="cvssVersion"
          renderAsEditable={props.isEditing}
          validate={[required]}
          visible={props.isEditing}
        >
          <option value="" selected={true} />
          <option value="2">2</option>
        </EditableField>
      </Row>
      {renderCVSSFields(props, cvssVersion)}
      <Row className={style.row}>
        {cvssVersion === "3"
          ? <Col md={3} xs={12} sm={12} className={style.title}><label><b>CVSS v3 Temporal</b></label></Col>
          : <Col md={3} xs={12} sm={12} className={style.title}><label><b>CVSS v2 Temporal</b></label></Col>
        }
        <Col md={9} xs={12} sm={12} className={style.desc}><p>{props.criticity}</p></Col>
      </Row>
    </React.Fragment>
  );
};

export const component: React.SFC<ISeverityViewProps> =
  (props: ISeverityViewProps): JSX.Element => (
    <React.StrictMode>
      <Row>
        <Col md={12} sm={12} xs={12}>
        <GenericForm
          name="editSeverity"
          initialValues={{...props.dataset, ...{cvssVersion: props.cvssVersion}}}
          onSubmit={(values: ISeverityViewProps["dataset"] & { cvssVersion: string }): void => {
                const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
                  store.dispatch as ThunkDispatch<{}, {}, AnyAction>
                );

                thunkDispatch(actions.updateSeverity(
                  props.findingId,
                  values,
                  props.criticity,
                ));
              }}
          onChange={(values: {}): void => {
                store.dispatch(actions.calcCVSSv2(values as ISeverityViewProps["dataset"]));
              }}
        >
          {renderSeverityFields(props)}
        </GenericForm>
        </Col>
      </Row>
    </React.StrictMode>
  );

const fieldSelector: ((state: {}, ...fields: string[]) => string) = formValueSelector("editSeverity");

export const severityView: React.ComponentType<ISeverityViewProps> = reduxWrapper(
  enhance(component) as React.SFC<ISeverityViewProps>,
  (state: StateType<Reducer>): ISeverityViewProps => ({
    ...state.dashboard.severity,
    formValues: { editSeverity: { values: { cvssVersion: fieldSelector(state, "cvssVersion") } } },
    isMdlConfirmOpen: state.dashboard.isMdlConfirmOpen,
  }),
);
