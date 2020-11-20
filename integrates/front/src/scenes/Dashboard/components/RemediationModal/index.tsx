/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the fields
 */

import _ from "lodash";
import React from "react";
import { Field, InjectedFormProps } from "redux-form";
import { ConfigurableValidator } from "revalidate";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  ButtonToolbar,
  ControlLabel,
  FormGroup,
  RequiredField,
} from "styles/styledComponents";
import { TextArea } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { maxLength, minLength, required } from "utils/validations";

export interface IAddRemediationProps {
  additionalInfo?: string;
  children?: React.ReactNode;
  isLoading: boolean;
  isOpen: boolean;
  maxJustificationLength?: number;
  message: string;
  title: string;
  onClose(): void;
  onSubmit(values: {}): void;
}

const minJustificationLength: ConfigurableValidator = minLength(10);
const remediationModal: React.FC<IAddRemediationProps> = (props: IAddRemediationProps): JSX.Element => {
  const { children, onClose, onSubmit } = props;

  const justificationValidations: ConfigurableValidator[] = [required, minJustificationLength];
  if (_.isNumber(props.maxJustificationLength)) {
    justificationValidations.push(maxLength(props.maxJustificationLength));
  }

  return (
    <React.StrictMode>
      <Modal
        open={props.isOpen}
        headerTitle={props.title}
      >
        <GenericForm name="updateRemediation" onSubmit={onSubmit}>
          {({ pristine }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              {children}
              <FormGroup>
                <ControlLabel>
                  <RequiredField>{"* "}</RequiredField>
                  {props.message}
                </ControlLabel>
                <Field
                  name="treatmentJustification"
                  type="text"
                  component={TextArea}
                  validate={justificationValidations}
                  withCount={true}
                  rows="6"
                />
              </FormGroup>
              {props.additionalInfo}
              <br />
              <ButtonToolbar>
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
