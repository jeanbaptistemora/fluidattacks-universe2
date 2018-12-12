/* tslint:disable jsx-no-lambda
 * Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 */
import React from "react";
import { Button, Col, Glyphicon, Row } from "react-bootstrap";
import { Provider } from "react-redux";
import { ConfigProps, DecoratedComponentClass, Field, InjectedFormProps, reduxForm } from "redux-form";
import store from "../../../../store/index";
import { fileInputField, textAreaField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import style from "./index.css";

interface IEvidenceImageProps {
  description: string;
  isDescriptionEditable: boolean;
  isEditing: boolean;
  name: string;
  url: string;
  onClick(): void;
  onUpdate(values: {}): void;
}

type formProps = IEvidenceImageProps & InjectedFormProps<{}, IEvidenceImageProps>;
const renderEditBox: ((props: formProps) => JSX.Element) =
  (props: formProps): JSX.Element => (
    <form onSubmit={props.handleSubmit}>
      <Field name={`${props.name}_filename`} id={props.name} component={fileInputField} />
      {props.isDescriptionEditable ? <Field name={`${props.name}_description`} component={textAreaField} /> : undefined}
      <Button bsStyle="success" block={true} type="submit" disabled={props.pristine || props.submitting}>
        <Glyphicon glyph="repeat" />
        &nbsp;{translate.t("search_findings.tab_evidence.update")}
      </Button>
    </form>
  );

type evidenceForm = DecoratedComponentClass<{}, IEvidenceImageProps & Partial<ConfigProps<{}, IEvidenceImageProps>>,
  string>;

const renderForm: ((props: IEvidenceImageProps) => JSX.Element) = (props: IEvidenceImageProps): JSX.Element => {
  /* tslint:disable-next-line:variable-name
   * Disabling here is necessary due a conflict
   * between lowerCamelCase var naming rule from tslint
   * and PascalCase rule for naming JSX elements
   */
  const Form: evidenceForm = reduxForm<{}, IEvidenceImageProps>({
    enableReinitialize: true,
    form: props.name,
  })(renderEditBox);

  return (
    <Provider store={store}>
      <Form
        {...props}
        onSubmit={(values: {}): void => { props.onUpdate(values); }}
        initialValues={{ [`${props.name}_description`]: props.description }}
      />
    </Provider>
  );
};

export const evidenceImage: React.SFC<IEvidenceImageProps> = (props: IEvidenceImageProps): JSX.Element => (
  <React.StrictMode>
    <Col md={4} sm={6} xs={12}>
      <div>
        <div className={style.imgContainer}>
          <img src={props.url} className={style.img} onClick={(): void => { props.onClick(); }} />
        </div>
        <div className={style.description}>
          <Row>
            <label><b>{translate.t("search_findings.tab_evidence.detail")}</b></label>
          </Row>
          <Row>
            {props.isEditing ? renderForm(props) : <p>{props.description}</p>}
          </Row>
        </div>
      </div>
    </Col>
  </React.StrictMode>
);
