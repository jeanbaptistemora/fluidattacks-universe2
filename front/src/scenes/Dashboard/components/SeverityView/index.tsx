/* tslint:disable jsx-no-lambda number-literal-format jsx-no-multiline-js
 * JSX-NO-LAMBDA: Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 *
 * JSX-NO-MULTILINE-JS: necessary for the sake of readability of the code that dynamically renders fields
 * as input or <p> depending on their state
 */

import _ from "lodash";
import React from "react";
import { Button, Col, Glyphicon, Row } from "react-bootstrap";
import { Provider } from "react-redux";
import { Reducer } from "redux";
import { ConfigProps, DecoratedComponentClass, Field, InjectedFormProps, reduxForm } from "redux-form";
import { StateType } from "typesafe-actions";
import store from "../../../../store/index";
import { dropdownField } from "../../../../utils/forms/fields";
import reduxWrapper from "../../../../utils/reduxWrapper";
import { translationsMap } from "../../../../utils/translations/formstackValues";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import * as actions from "../../actions";
import style from "./index.css";

export interface ISeverityViewProps {
  criticity: number;
  cssv2base: number;
  dataset: {
    accessComplexity: string;
    accessVector: string;
    authentication: string;
    availabilityImpact: string;
    confidenceLevel: string;
    confidentialityImpact: string;
    exploitability: string;
    integrityImpact: string;
    resolutionLevel: string;
  };
  findingId: string;
  isEditing: boolean;
  onUpdate(values: ISeverityViewProps["dataset"]): void;
}

interface ISeverityField {
  currentValue: string;
  name: string;
  options: Array<{ text: string; value: string }>;
  title: string;
}

type formProps = ISeverityViewProps & InjectedFormProps<{}, ISeverityViewProps>;

const renderEditPanel: ((arg1: formProps) => JSX.Element) = (props: formProps): JSX.Element => (
  <Row ng-show="isManager">
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

const renderFields: React.SFC<formProps> = (props: formProps): JSX.Element => {

  const fields: ISeverityField[] = [
    {
      currentValue: props.dataset.accessVector, name: "accessVector",
      options: [
        { text: "search_findings.tab_severity.vector_options.local", value: "0.395" },
        { text: "search_findings.tab_severity.vector_options.adjacent", value: "0.646" },
        { text: "search_findings.tab_severity.vector_options.network", value: "1.000" },
      ],
      title: translate.t("search_findings.tab_severity.vector"),
    },
    {
      currentValue: props.dataset.confidentialityImpact, name: "confidentialityImpact",
      options: [
        { text: "search_findings.tab_severity.confidentiality_options.none", value: "0" },
        { text: "search_findings.tab_severity.confidentiality_options.partial", value: "0.275" },
        { text: "search_findings.tab_severity.confidentiality_options.complete", value: "0.660" },
      ],
      title: translate.t("search_findings.tab_severity.confidentiality"),
    },
    {
      currentValue: props.dataset.integrityImpact, name: "integrityImpact",
      options: [
        { text: "search_findings.tab_severity.integrity_options.none", value: "0" },
        { text: "search_findings.tab_severity.integrity_options.partial", value: "0.275" },
        { text: "search_findings.tab_severity.integrity_options.complete", value: "0.660" },
      ],
      title: translate.t("search_findings.tab_severity.integrity"),
    },
    {
      currentValue: props.dataset.availabilityImpact, name: "availabilityImpact",
      options: [
        { text: "search_findings.tab_severity.availability_options.none", value: "0" },
        { text: "search_findings.tab_severity.availability_options.partial", value: "0.275" },
        { text: "search_findings.tab_severity.availability_options.complete", value: "0.660" },
      ],
      title: translate.t("search_findings.tab_severity.availability"),
    },
    {
      currentValue: props.dataset.authentication, name: "authentication",
      options: [
        { text: "search_findings.tab_severity.authentication_options.multiple_auth", value: "0.450" },
        { text: "search_findings.tab_severity.authentication_options.single_auth", value: "0.560" },
        { text: "search_findings.tab_severity.authentication_options.no_auth", value: "0.704" },
      ],
      title: translate.t("search_findings.tab_severity.authentication"),
    },
    {
      currentValue: props.dataset.exploitability, name: "exploitability",
      options: [
        { text: "search_findings.tab_severity.exploitability_options.improbable", value: "0.850" },
        { text: "search_findings.tab_severity.exploitability_options.conceptual", value: "0.900" },
        { text: "search_findings.tab_severity.exploitability_options.functional", value: "0.950" },
        { text: "search_findings.tab_severity.exploitability_options.high", value: "1.000" },
      ],
      title: translate.t("search_findings.tab_severity.exploitability"),
    },
    {
      currentValue: props.dataset.confidenceLevel, name: "confidenceLevel",
      options: [
        { text: "search_findings.tab_severity.confidence_options.not_confirm", value: "0.900" },
        { text: "search_findings.tab_severity.confidence_options.not_corrob", value: "0.950" },
        { text: "search_findings.tab_severity.confidence_options.confirmed", value: "1.000" },
      ],
      title: translate.t("search_findings.tab_severity.confidence"),
    },
    {
      currentValue: props.dataset.resolutionLevel, name: "resolutionLevel",
      options: [
        { text: "search_findings.tab_severity.resolution_options.official", value: "0.870" },
        { text: "search_findings.tab_severity.resolution_options.temporal", value: "0.900" },
        { text: "search_findings.tab_severity.resolution_options.palliative", value: "0.950" },
        { text: "search_findings.tab_severity.resolution_options.non_existent", value: "1.000" },
      ],
      title: translate.t("search_findings.tab_severity.resolution"),
    },
    {
      currentValue: props.dataset.accessComplexity, name: "accessComplexity",
      options: [
        { text: "search_findings.tab_severity.complexity_options.high_complex", value: "0.350" },
        { text: "search_findings.tab_severity.complexity_options.medium_complex", value: "0.610" },
        { text: "search_findings.tab_severity.complexity_options.low_complex", value: "0.710" },
      ],
      title: translate.t("search_findings.tab_severity.complexity"),
    },
  ];

  return (
    <React.StrictMode>
      <form onSubmit={props.handleSubmit}>
        {renderEditPanel(props)}
        {fields.map((field: ISeverityField, index: number) => {
          const value: string = field.currentValue.split(" | ")[0];
          const text: string = field.currentValue.split(" | ")[1];

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
                    {field.options.map((option: ISeverityField["options"][0]) => (
                      <option value={`${option.value} | ${translate.t(option.text, { lng: "es" })}`}>
                        {translate.t(option.text)}
                      </option>
                    ))}
                  </Field>
                  : <p className={style.desc}>{value} | {translate.t(translationsMap[text])}</p>
                }
              </Col>
            </Row>
          );
        })}
      </form>
    </React.StrictMode>
  );
};

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
      {_.isEmpty(props.dataset.accessComplexity) ? <div /> :
        <Row>
          <Col md={12} sm={12} xs={12}>
            <Provider store={store}>
              <Form
                {...props}
                onChange={(values: {}): void => { store.dispatch(actions.calcCVSSv2(values)); }}
                initialValues={props.dataset}
                onSubmit={(values: {}): void => {
                  props.onUpdate(_.merge(
                    values as ISeverityViewProps["dataset"],
                    { criticity: props.criticity, id: props.findingId  },
                  ));
                }}
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
      }
    </React.StrictMode>
  );

export const severityView: React.ComponentType<ISeverityViewProps> = reduxWrapper(
  component, (state: StateType<Reducer>, ownProps: ISeverityViewProps): ISeverityViewProps => ({
    ...state.dashboard.severity,
    criticity: state.dashboard.severity.criticity === 0 ? ownProps.criticity : state.dashboard.severity.criticity,
    cssv2base: state.dashboard.severity.cssv2base === 0 ? ownProps.cssv2base : state.dashboard.severity.cssv2base,
  }),
);
