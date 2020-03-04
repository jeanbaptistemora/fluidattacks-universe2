/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the fields
 */

import React from "react";
import { ButtonToolbar, ControlLabel, FormGroup } from "react-bootstrap";
import { Field, InjectedFormProps } from "redux-form";
import { ConfigurableValidator } from "revalidate";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import { default as globalStyle } from "../../../../styles/global.css";
import { textAreaField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { minLength, required } from "../../../../utils/validations";
import { GenericForm } from "../GenericForm";

export interface IAddRemediationProps {
  additionalInfo?: string;
  isLoading: boolean;
  isOpen: boolean;
  message: string;
  title: string;
  children?(): JSX.Element;
  onClose(): void;
  onSubmit(values: {}): void;
}

const minJustificationLength: ConfigurableValidator = minLength(50);
const remediationModal: React.FC<IAddRemediationProps> = (props: IAddRemediationProps): JSX.Element => {
  const { onClose, onSubmit } = props;

  return (
    <React.StrictMode>
      <Modal
        open={props.isOpen}
        headerTitle={props.title}
        footer={<div />}
      >
        <GenericForm name="updateRemediation" onSubmit={onSubmit}>
          {({ pristine }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              {props.children === undefined ? undefined : props.children()}
              <FormGroup>
                <ControlLabel>
                  <label style={{ color: "#f22" }}>* </label>
                  {props.message}
                </ControlLabel>
                <Field
                  name="treatmentJustification"
                  type="text"
                  className={globalStyle.noResize}
                  component={textAreaField}
                  validate={[required, minJustificationLength]}
                  withCount={true}
                  rows="6"
                />
              </FormGroup>
              {props.additionalInfo}
              <br />
              <ButtonToolbar className="pull-right">
                <Button onClick={onClose}>
                  {translate.t("confirmmodal.cancel")}
                </Button>
                <Button type="submit" disabled={pristine || props.isLoading}>
                  {translate.t("confirmmodal.proceed")}
                </Button>
              </ButtonToolbar>
            </React.Fragment>
          )}
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};

export { remediationModal as RemediationModal };
