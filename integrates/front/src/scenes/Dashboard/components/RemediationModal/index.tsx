import { Field, Form, Formik } from "formik";
import _ from "lodash";
import React from "react";
import type { ConfigurableValidator } from "revalidate";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { FormikTextArea } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
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
const RemediationModal: React.FC<IAddRemediationProps> = (
  props: IAddRemediationProps
): JSX.Element => {
  const {
    additionalInfo,
    children,
    isOpen,
    maxJustificationLength,
    message,
    title,
    onClose,
    onSubmit,
  } = props;

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
      <Modal headerTitle={title} onClose={onClose} open={isOpen}>
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
                <br />
                <hr />
                <Row>
                  <Col100>
                    <ButtonToolbar>
                      <Button
                        id={"cancel-remediation"}
                        onClick={onClose}
                        variant={"secondary"}
                      >
                        {translate.t("confirmmodal.cancel")}
                      </Button>
                      <Button
                        disabled={!dirty || props.isLoading}
                        id={"proceed-remediation"}
                        type={"submit"}
                        variant={"primary"}
                      >
                        {translate.t("confirmmodal.proceed")}
                      </Button>
                    </ButtonToolbar>
                  </Col100>
                </Row>
              </React.Fragment>
            </Form>
          )}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { RemediationModal, IAddRemediationProps };
