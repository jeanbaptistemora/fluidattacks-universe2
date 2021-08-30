import { useMutation } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { DEACTIVATE_ROOT } from "./queries";

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
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface IDeactivationModalProps {
  groupName: string;
  rootId: string;
  onClose: () => void;
  onUpdate: () => void;
}

export const DeactivationModal: React.FC<IDeactivationModalProps> = ({
  groupName,
  rootId,
  onClose,
  onUpdate,
}: IDeactivationModalProps): JSX.Element => {
  const { t } = useTranslation();

  const [deactivateRoot] = useMutation(DEACTIVATE_ROOT, {
    onCompleted: (): void => {
      onClose();
      onUpdate();
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        if (
          error.message ===
          "Exception - A root with open vulns can't be deactivated"
        ) {
          msgError(t("group.scope.common.errors.hasOpenVulns"));
        } else {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.error("Couldn't deactivate root", error);
        }
      });
    },
  });

  const validations = object().shape({
    other: string().when("reason", {
      is: "OTHER",
      then: string().required(t("validations.required")),
    }),
    reason: string().required(t("validations.required")),
  });

  const handleSubmit = useCallback(
    async (values: Record<string, string>): Promise<void> => {
      await deactivateRoot({
        variables: {
          groupName,
          id: rootId,
          other: values.other,
          reason: values.reason,
        },
      });
    },
    [deactivateRoot, groupName, rootId]
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
