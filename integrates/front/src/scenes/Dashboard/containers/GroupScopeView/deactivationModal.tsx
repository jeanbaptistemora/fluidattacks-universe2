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
import { FormikDropdown, FormikText } from "utils/forms/fields";

interface IDeactivationModalProps {
  rootId: string;
  onClose: () => void;
  onSubmit: (rootId: string, values: Record<string, string>) => Promise<void>;
}

export const DeactivationModal: React.FC<IDeactivationModalProps> = ({
  rootId,
  onClose,
  onSubmit,
}: IDeactivationModalProps): JSX.Element => {
  const { t } = useTranslation();

  const validations = object().shape({
    other: string().when("reason", {
      is: "OTHER",
      then: string().required(t("validations.required")),
    }),
    reason: string().required(t("validations.required")),
  });

  const handleSubmit = useCallback(
    async (values: Record<string, string>): Promise<void> => {
      await onSubmit(rootId, values);
    },
    [onSubmit, rootId]
  );

  return (
    <React.StrictMode>
      <Modal
        headerTitle={t("group.scope.common.deactivation.title")}
        onEsc={onClose}
        open={true}
      >
        <Formik
          initialValues={{ other: "", reason: "" }}
          onSubmit={handleSubmit}
          validationSchema={validations}
        >
          {({ dirty, isSubmitting, values }): JSX.Element => (
            <Form>
              <Row>
                <Col100>
                  <FormGroup>
                    <ControlLabel>
                      {t("group.scope.common.deactivation.reason.label")}
                    </ControlLabel>
                    <Field component={FormikDropdown} name={"reason"}>
                      <option value={""} />
                      <option value={"OUT_OF_SCOPE"}>
                        {t("group.scope.common.deactivation.reason.scope")}
                      </option>
                      <option value={"REGISTERED_BY_MISTAKE"}>
                        {t("group.scope.common.deactivation.reason.mistake")}
                      </option>
                      <option value={"MOVED_TO_ANOTHER_ROOT"}>
                        {t("group.scope.common.deactivation.reason.moved")}
                      </option>
                      <option value={"OTHER"}>
                        {t("group.scope.common.deactivation.reason.other")}
                      </option>
                    </Field>
                  </FormGroup>
                  {values.reason === "OTHER" ? (
                    <FormGroup>
                      <ControlLabel>
                        {t("group.scope.common.deactivation.other")}
                      </ControlLabel>
                      <Field component={FormikText} name={"other"} />
                    </FormGroup>
                  ) : undefined}
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
