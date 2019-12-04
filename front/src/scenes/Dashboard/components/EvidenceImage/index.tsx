/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that renders the form
 */
import React from "react";
import { Col, Row } from "react-bootstrap";
import { Field, InjectedFormProps, Validator } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import { fileInputField, textAreaField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import { GenericForm } from "../GenericForm";
import { default as style } from "./index.css";

interface IEvidenceImageProps {
  acceptedMimes?: string;
  content: string | JSX.Element;
  description: string;
  isDescriptionEditable: boolean;
  isEditing: boolean;
  name: string;
  validate?: Validator | Validator[];
  onClick(): void;
  onUpdate(values: {}): void;
}

const renderDescriptionField: ((name: string) => JSX.Element) = (name: string): JSX.Element => (
  <Field name={`${name}_description`} component={textAreaField} validate={[required]} />
);

const renderForm: ((props: IEvidenceImageProps) => JSX.Element) = (props: IEvidenceImageProps): JSX.Element => {
  const handleSubmit: ((values: {}) => void) = (values: {}): void => { props.onUpdate(values); };

  return (
    <GenericForm
      name={props.name}
      onSubmit={handleSubmit}
      initialValues={{ [`${props.name}_description`]: props.description }}
    >
      {({ pristine, submitting }: InjectedFormProps): JSX.Element => (
        <React.Fragment>
          <Field
            name={`${props.name}_filename`}
            id={props.name}
            component={fileInputField}
            accept={props.acceptedMimes}
            validate={props.validate}
          />
          {props.isDescriptionEditable ? renderDescriptionField(props.name) : <p>{props.description}</p>}
          <Button bsStyle="success" block={true} type="submit" disabled={pristine || submitting}>
            <FluidIcon icon="loading" />
            &nbsp;{translate.t("search_findings.tab_evidence.update")}
          </Button>
        </React.Fragment>
      )}
    </GenericForm>
  );
};

export const evidenceImage: React.FC<IEvidenceImageProps> = (props: IEvidenceImageProps): JSX.Element => {
  const handleClick: (() => void) = (): void => { props.onClick(); };

  return (
    <React.StrictMode>
      <Col md={4} sm={6} xs={12}>
        <div>
          <div className={style.imgContainer}>
            {typeof (props.content) === "string"
              ? <img src={props.content} className={style.img} onClick={handleClick} />
              : React.cloneElement(props.content, { className: style.img, onClick: handleClick })}
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
};
