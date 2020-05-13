/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that renders the form
 */
import React from "react";
import { Col, Row } from "react-bootstrap";
import { Field, FormSection, Validator } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import { fileInputField, textAreaField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { validEvidenceDescription, validTextField } from "../../../../utils/validations";
import { default as style } from "./index.css";

interface IEvidenceImageProps {
  acceptedMimes?: string;
  content: string | JSX.Element;
  description: string;
  isDescriptionEditable: boolean;
  isEditing: boolean;
  isRemovable?: boolean;
  name: string;
  validate?: Validator | Validator[];
  onClick(): void;
  onDelete?(): void;
}

const renderForm: ((props: IEvidenceImageProps) => JSX.Element) = (props: IEvidenceImageProps): JSX.Element => {
  const { onDelete } = props;

  return (
    <FormSection name={props.name}>
      <Field
        name="file"
        id={props.name}
        component={fileInputField}
        accept={props.acceptedMimes}
        validate={props.validate}
      />
      {props.isDescriptionEditable
        ?
          <Field
            name="description"
            component={textAreaField}
            validate={[validEvidenceDescription, validTextField]}
          />
        : <p>{props.description}</p>}
      {props.isRemovable === true
        ? <Button bsStyle="success" block={true} onClick={onDelete}>
          <FluidIcon icon="delete" />
          &nbsp;{translate.t("search_findings.tab_evidence.remove")}
        </Button>
        : undefined}
    </FormSection>
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
