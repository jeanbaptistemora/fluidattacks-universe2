/* tslint:disable jsx-no-lambda number-literal-format jsx-no-multiline-js
 * JSX-NO-LAMBDA: Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 *
 * JSX-NO-MULTILINE-JS: necessary for the sake of readability of the code that dynamically renders fields
 * as input or <p> depending on their state
 */

import React from "react";
import { Button, Col, Glyphicon, Row } from "react-bootstrap";
import { Provider } from "react-redux";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { AnyAction, Reducer } from "redux";
import { ConfigProps, DecoratedComponentClass, Field, InjectedFormProps, reduxForm } from "redux-form";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { confirmDialog as ConfirmDialog } from "../../../../components/ConfirmDialog/index";
import store from "../../../../store/index";
import { castFields } from "../../../../utils/formatHelpers";
import { dropdownField } from "../../../../utils/forms/fields";
import reduxWrapper from "../../../../utils/reduxWrapper";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import * as actions from "../../actions";
import style from "./index.css";

export interface ISeverityViewProps {
  canEdit: boolean;
  criticity: number;
  cssv2base: number;
  dataset: {
    accessComplexity: string;
    accessVector: string;
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
    resolutionLevel: string;
  };
  findingId: string;
  formValues: { editSeverity: { values: ISeverityViewProps["dataset"] }};
  isEditing: boolean;
  isMdlConfirmOpen: boolean;
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

type formProps = ISeverityViewProps & InjectedFormProps<{}, ISeverityViewProps>;

const renderEditPanel: ((arg1: formProps) => JSX.Element) = (props: formProps): JSX.Element => (
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
          <Button bsStyle="success" block={true} type="submit">
            <Glyphicon glyph="repeat" /> {translate.t("search_findings.tab_severity.update")}
          </Button>
        </Col>
      </Row>
      : undefined
    }
  </Row>
);

const renderFields: React.SFC<formProps> = (props: formProps): JSX.Element => (
  <React.StrictMode>
    <form onSubmit={props.handleSubmit}>
      {props.canEdit ? renderEditPanel(props) : undefined}
      {castFields(props.dataset)
        .map((field: ISeverityField, index: number) => {
        const value: string = field.currentValue;
        const text: string = field.options[value];

        return (
          <Row className={style.row} key={index}>
            <Col md={3} xs={12} sm={12} className={style.title}><label><b>{field.title}</b></label></Col>
            <Col md={9} xs={12} sm={12}>
              {props.isEditing
                ?
                <Field
                  name={field.name}
                  component={dropdownField}
                  validate={[required]}
                  onChange={(): void => undefined}
                >
                  <option value="" selected={true} />
                  {Object.keys(field.options)
                    .map((key: string) => (
                    <option value={`${key}`}>
                      {translate.t(field.options[key])}
                    </option>
                  ))}
                </Field>
                : <p className={style.desc}>{value} | {translate.t(text)}</p>
              }
            </Col>
          </Row>
        );
      })}
    </form>
  </React.StrictMode>
);

type severityForm = DecoratedComponentClass<{}, ISeverityViewProps & Partial<ConfigProps<{}, ISeverityViewProps>>,
  string>;

/* tslint:disable-next-line:variable-name
 * Disabling here is necessary due a conflict
 * between lowerCamelCase var naming rule from tslint
 * and PascalCase rule for naming JSX elements
 */
const Form: severityForm = reduxForm<{}, ISeverityViewProps>({
  enableReinitialize: true,
  form: "editSeverity",
})(renderFields);

export const component: React.SFC<ISeverityViewProps> =
  (props: ISeverityViewProps): JSX.Element => (
    <React.StrictMode>
      <Row>
        <Col md={12} sm={12} xs={12}>
          <Provider store={store}>
            <Form
              {...props}
              onChange={(values: {}): void => { store.dispatch(actions.calcCVSSv2(values)); }}
              initialValues={props.dataset}
              onSubmit={(): void => { store.dispatch(actions.openConfirmMdl()); }}
            />
          </Provider>
          <Row className={style.row}>
            <Col md={3} xs={12} sm={12} className={style.title}><label><b>CVSS v2 Base</b></label></Col>
            <Col md={9} xs={12} sm={12} className={style.desc}><p>{props.cssv2base}</p></Col>
          </Row>
          <Row className={style.row}>
            <Col md={3} xs={12} sm={12} className={style.title}><label><b>CVSS v2 Temporal</b></label></Col>
            <Col md={9} xs={12} sm={12} className={style.desc}><p>{props.criticity}</p></Col>
          </Row>
        </Col>
      </Row>

      <ConfirmDialog
        open={props.isMdlConfirmOpen}
        title={translate.t("confirmmodal.title_cvssv2")}
        onProceed={(): void => {
          const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
            store.dispatch as ThunkDispatch<{}, {}, AnyAction>
          );

          thunkDispatch(actions.updateSeverity(
            props.findingId,
            props.formValues.editSeverity.values,
            props.criticity,
          ));
        }}
        onCancel={(): void => { store.dispatch(actions.closeConfirmMdl()); }}
      />
    </React.StrictMode>
  );

export const severityView: React.ComponentType<ISeverityViewProps> = reduxWrapper(
  enhance(component) as React.SFC<ISeverityViewProps>,
  (state: StateType<Reducer>): ISeverityViewProps => ({
    ...state.dashboard.severity,
    formValues: state.form,
    isMdlConfirmOpen: state.dashboard.isMdlConfirmOpen,
  }),
);
