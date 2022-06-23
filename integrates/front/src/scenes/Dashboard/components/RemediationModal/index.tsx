import { Field, Form, Formik } from "formik";
import _ from "lodash";
import React from "react";
import type { ConfigurableValidator } from "revalidate";

import { Modal, ModalConfirm } from "components/Modal";
import {
  ControlLabel,
  FormGroup,
  RequiredField,
} from "styles/styledComponents";
import { FormikTextArea } from "utils/forms/fields";
import {
  composeValidators,
  maxLength,
  minLength,
  required,
  validTextField,
} from "utils/validations";

// ESLint annotations needed in order to avoid the mutations of defaultProps
interface IAddRemediationProps {
  additionalInfo?: string; // eslint-disable-line react/require-default-props
  children?: React.ReactNode; // eslint-disable-line react/require-default-props
  isLoading: boolean;
  isOpen: boolean;
  maxJustificationLength?: number; // eslint-disable-line react/require-default-props
  message: string;
  title: string;
  onClose: () => void;
  onSubmit: (values: any) => void; // eslint-disable-line @typescript-eslint/no-explicit-any
}

const MIN_LENGTH: number = 10;
const minJustificationLength: ConfigurableValidator = minLength(MIN_LENGTH);
const RemediationModal: React.FC<IAddRemediationProps> = ({
  additionalInfo,
  children,
  isLoading,
  isOpen,
  maxJustificationLength,
  message,
  title,
  onClose,
  onSubmit,
}: IAddRemediationProps): JSX.Element => {
  const justificationValidations: ConfigurableValidator[] = [
    required,
    validTextField,
    minJustificationLength,
  ];
  if (_.isNumber(maxJustificationLength)) {
    // Next annotation needed in order to use push()
    // eslint-disable-next-line fp/no-mutating-methods
    justificationValidations.push(maxLength(maxJustificationLength));
  }

  return (
    <React.StrictMode>
      <Modal onClose={onClose} open={isOpen} title={title}>
        <Formik
          initialValues={{
            treatmentJustification: "",
          }}
          name={"updateRemediation"}
          onSubmit={onSubmit}
        >
          {({ dirty }): JSX.Element => (
            <Form>
              <React.Fragment>
                {children}
                <FormGroup>
                  <ControlLabel>
                    <RequiredField>{"* "}</RequiredField>
                    {message}
                  </ControlLabel>
                  <Field
                    component={FormikTextArea}
                    name={"treatmentJustification"}
                    rows={"6"}
                    type={"text"}
                    validate={composeValidators(justificationValidations)}
                    withCount={true}
                  />
                </FormGroup>
                {additionalInfo}
                <ModalConfirm
                  disabled={!dirty || isLoading}
                  id={"remediation-confirm"}
                  onCancel={onClose}
                />
              </React.Fragment>
            </Form>
          )}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export type { IAddRemediationProps };
export { RemediationModal };
