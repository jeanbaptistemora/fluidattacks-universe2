/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { Field, Form, Formik } from "formik";
import _ from "lodash";
import type { FC } from "react";
import React, { Fragment, StrictMode } from "react";
import type { ConfigurableValidator } from "revalidate";

import { Label } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { FormGroup } from "styles/styledComponents";
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
const RemediationModal: FC<IAddRemediationProps> = ({
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
                <FormGroup>
                  <Label required={true}>{message}</Label>
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
