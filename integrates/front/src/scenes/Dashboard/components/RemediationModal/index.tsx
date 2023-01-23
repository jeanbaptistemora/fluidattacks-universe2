import { Form, Formik } from "formik";
import _ from "lodash";
import React, { Fragment, StrictMode } from "react";
import type { ConfigurableValidator } from "revalidate";

import { TextArea } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import {
  composeValidators,
  maxLength,
  minLength,
  required,
  validTextField,
} from "utils/validations";

interface IAddRemediationProps {
  additionalInfo?: string;
  children?: React.ReactNode;
  isLoading: boolean;
  isOpen: boolean;
  maxJustificationLength?: number;
  message: string;
  title: string;
  onClose: () => void;
  onSubmit: (values: { treatmentJustification: string }) => void;
}

const MIN_LENGTH: number = 10;
const minJustificationLength: ConfigurableValidator = minLength(MIN_LENGTH);

const RemediationModal: React.FC<Readonly<IAddRemediationProps>> = ({
  additionalInfo,
  children,
  isLoading,
  isOpen,
  maxJustificationLength,
  message,
  title,
  onClose,
  onSubmit,
}): JSX.Element => {
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
    <StrictMode>
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
              <Fragment>
                {children}
                <TextArea
                  count={true}
                  label={message}
                  name={"treatmentJustification"}
                  required={true}
                  rows={6}
                  validate={composeValidators(justificationValidations)}
                />
                {additionalInfo}
                <ModalConfirm
                  disabled={!dirty || isLoading}
                  id={"remediation-confirm"}
                  onCancel={onClose}
                />
              </Fragment>
            </Form>
          )}
        </Formik>
      </Modal>
    </StrictMode>
  );
};

export type { IAddRemediationProps };
export { RemediationModal };
