/* tslint:disable jsx-no-lambda number-literal-format jsx-no-multiline-js
 * JSX-NO-LAMBDA: Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 *
 * JSX-NO-MULTILINE-JS: necessary for the sake of readability of the code that dynamically renders fields
 * as input or <p> depending on their state
 */

import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { AnyAction, Reducer } from "redux";
import { formValueSelector, submit } from "redux-form";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { Button } from "../../../../components/Button/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import store from "../../../../store/index";
import { castEnvironmentCVSS3Fields, castFieldsCVSS3, castPrivileges } from "../../../../utils/formatHelpers";
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
  cvssVersion: string;
  dataset: {
    attackComplexity: string;
    attackVector: string;
    availabilityImpact: string;
    availabilityRequirement: string;
    confidentialityImpact: string;
    confidentialityRequirement: string;
    exploitability: string;
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
    severityScope: string;
    userInteraction: string;
  };
  findingId: string;
  formValues: {
    editSeverity: {
      values: {
        cvssVersion: string;
        modifiedSeverityScope: string;
        severityScope: string;
      };
    };
  };
  isEditing: boolean;
  severity: number;
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
    mixpanel.track(
      "FindingSeverity",
      {
        Organization: (window as Window & { userOrganization: string }).userOrganization,
        User: (window as Window & { userName: string }).userName,
      });
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
        <Button
          bsStyle="primary"
          block={true}
          onClick={(): void => {
            store.dispatch(actions.editSeverity());
            store.dispatch(actions.calcCVSS(props.dataset, props.cvssVersion));
          }}
        >
          <FluidIcon icon="edit" /> {translate.t("search_findings.tab_severity.editable")}
        </Button>
      </Col>
    </Row>
    <br />
    {props.isEditing
      ?
      <Row>
        <Col md={2} mdOffset={10} xs={12} sm={12}>
          <Button bsStyle="success" block={true} type="submit" onClick={(): void => { submit("editSeverity"); }}>
            <FluidIcon icon="loading" /> {translate.t("search_findings.tab_severity.update")}
          </Button>
        </Col>
      </Row>
      : undefined
    }
  </Row>
);

const renderCVSSFields: ((props: ISeverityViewProps) => JSX.Element[]) =
  (props: ISeverityViewProps): JSX.Element[] =>
  castFieldsCVSS3(props.dataset)
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

const renderEnvironmentFields: ((props: ISeverityViewProps) => JSX.Element[]) =
  (props: ISeverityViewProps): JSX.Element[] =>
  castEnvironmentCVSS3Fields(props.dataset)
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
              visible={props.isEditing}
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

  const severityScope: string = (props.isEditing)
    ? props.formValues.editSeverity.values.severityScope
    : props.dataset.severityScope;

  const modifiedSeverityScope: string = (props.isEditing)
    ? props.formValues.editSeverity.values.modifiedSeverityScope
    : props.dataset.modifiedSeverityScope;

  const privilegesOptions: {[value: string]: string} = castPrivileges(severityScope);
  const modPrivilegesOptions: {[value: string]: string} = castPrivileges(modifiedSeverityScope);

  const privileges: string = props.dataset.privilegesRequired;
  const modPrivileges: string = props.dataset.modifiedPrivilegesRequired;

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
          <option value="3">3</option>
        </EditableField>
      </Row>
      {renderCVSSFields(props)}
      <Row className={style.row}>
        <EditableField
          alignField="horizontal"
          component={dropdownField}
          currentValue={`${privileges} | ${translate.t(privilegesOptions[privileges])}`}
          label={translate.t("search_findings.tab_severity.privileges_required")}
          name="privilegesRequired"
          renderAsEditable={props.isEditing}
          validate={[required]}
        >
          <option value="" selected={true} />
          {Object.keys(privilegesOptions)
            .map((key: string) => (
            <option value={`${key}`}>
              {translate.t(privilegesOptions[key])}
            </option>
          ))}
        </EditableField>
      </Row>
      { cvssVersion === "3" && props.isEditing
        ?
        <React.Fragment>
          {renderEnvironmentFields(props)}
          <Row className={style.row}>
            <EditableField
              alignField="horizontal"
              component={dropdownField}
              currentValue={`${modPrivileges} | ${translate.t(modPrivilegesOptions[modPrivileges])}`}
              label={translate.t("search_findings.tab_severity.modified_privileges_required")}
              name="modifiedPrivilegesRequired"
              renderAsEditable={props.isEditing}
              validate={[required]}
              visible={props.isEditing}
            >
              <option value="" selected={true} />
              {Object.keys(modPrivilegesOptions)
                .map((key: string) => (
                <option value={`${key}`}>
                  {translate.t(modPrivilegesOptions[key])}
                </option>
              ))}
            </EditableField>
          </Row>
        </React.Fragment>
        : undefined
      }
      <Row className={style.row}>
        <Col md={3} xs={12} sm={12} className={style.title}><label><b>CVSS v3 Temporal</b></label></Col>
        <Col md={9} xs={12} sm={12} className={style.desc}><p>{props.severity}</p></Col>
      </Row>
    </React.Fragment>
  );
};

export const component: React.FC<ISeverityViewProps> =
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
                mixpanel.track(
                  "UpdateSeverity",
                  {
                    Organization: (window as Window & { userOrganization: string }).userOrganization,
                    User: (window as Window & { userName: string }).userName,
                  });
                thunkDispatch(actions.updateSeverity(
                  props.findingId,
                  values,
                  props.severity,
                ));
              }}
          onChange={(values: ISeverityViewProps["dataset"] & {cvssVersion: string}): void => {
                store.dispatch(actions.calcCVSS(values as ISeverityViewProps["dataset"], values.cvssVersion));
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
  enhance(component) as React.FC<ISeverityViewProps>,
  (state: StateType<Reducer>): ISeverityViewProps => ({
    ...state.dashboard.severity,
    formValues: {
      editSeverity: {
        values: {
          cvssVersion: fieldSelector(state, "cvssVersion"),
          modifiedSeverityScope: fieldSelector(state, "modifiedSeverityScope"),
          severityScope: fieldSelector(state, "severityScope"),
        },
      },
    },
    isMdlConfirmOpen: state.dashboard.isMdlConfirmOpen,
  }),
);
