import { Field, Form, Formik } from "formik";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { FormikDropdown } from "utils/forms/fields";

interface IDeactivationModalProps {
  rootId: string;
  onClose: () => void;
  onSubmit: (rootId: string, reason: string) => Promise<void>;
}

export const DeactivationModal: React.FC<IDeactivationModalProps> = ({
  rootId,
  onClose,
  onSubmit,
}: IDeactivationModalProps): JSX.Element => {
  const { t } = useTranslation();

  const validations = object().shape({
    reason: string().required(t("validations.required")),
  });

  const handleSubmit = useCallback(
    async (values: { reason: string }): Promise<void> => {
      await onSubmit(rootId, values.reason);
    },
    [onSubmit, rootId]
  );

  return (
    <React.StrictMode>
      <Modal headerTitle={t("scope.common.deactivation.title")} open={true}>
        <Formik
          initialValues={{ reason: "" }}
          onSubmit={handleSubmit}
          validationSchema={validations}
        >
          {({ dirty, isSubmitting }): JSX.Element => (
            <Form>
              <Row>
                <Col100>
                  <FormGroup>
                    <ControlLabel>
                      {t("scope.common.deactivation.reason")}
                    </ControlLabel>
                    <Field component={FormikDropdown} name={"reason"}>
                      <option value={""} />
                      <option value={"CODE_EXITS_THE_PROJECT"}>
                        {t("scope.common.deactivation.reason.exits")}
                      </option>
                      <option value={"REGISTERED_BY_MISTAKE"}>
                        {t("scope.common.deactivation.reason.mistake")}
                      </option>
                    </Field>
                  </FormGroup>
                </Col100>
              </Row>
              <Row>
                <Col100>
                  <ButtonToolbar>
                    <Button onClick={onClose}>
                      {t("confirmmodal.cancel")}
                    </Button>
                    <Button disabled={!dirty || isSubmitting} type={"submit"}>
                      {t("confirmmodal.proceed")}
                    </Button>
                  </ButtonToolbar>
                </Col100>
              </Row>
            </Form>
          )}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};
