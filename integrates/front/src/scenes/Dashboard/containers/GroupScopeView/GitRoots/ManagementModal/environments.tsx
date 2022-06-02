import { Field, Form, Formik } from "formik";
import _ from "lodash";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { array, object, string } from "yup";

import type { IGitRootAttr } from "../../types";
import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Button } from "components/Button";
import { ModalFooter } from "components/Modal";
import {
  ControlLabel,
  FormGroup,
  RequiredField,
} from "styles/styledComponents";
import {
  FormikArrayField,
  FormikDropdown,
  FormikText,
} from "utils/forms/fields";

interface IEnvironmentsProps {
  rootInitialValues: IGitRootAttr;
  modalMessages: { message: string; type: string };
  onClose: () => void;
  onSubmit: (values: IGitRootAttr) => Promise<void>;
}

const Environments: React.FC<IEnvironmentsProps> = ({
  rootInitialValues,
  modalMessages,
  onClose,
  onSubmit,
}: IEnvironmentsProps): JSX.Element => {
  const { t } = useTranslation();

  const [deletedUrls, setDeletedUrls] = useState(false);
  const [showAlert, setShowAlert] = useState(false);

  const validations = object().shape({
    environmentUrls: array().of(string().required(t("validations.required"))),
    other: string().when("reason", {
      is: "OTHER",
      otherwise: string(),
      then: string().required(t("validations.required")),
    }),
    reason: string().test(
      "hasDeletedUrls",
      t("validations.required"),
      (value): boolean => {
        return !deletedUrls || !_.isEmpty(value);
      }
    ),
  });
  const initialValues = { ...rootInitialValues, other: "", reason: "" };

  return (
    <Formik
      initialValues={initialValues}
      name={"gitEnvs"}
      onSubmit={onSubmit}
      validationSchema={validations}
    >
      {({ dirty, isSubmitting, values }): JSX.Element => {
        if (isSubmitting) {
          setShowAlert(false);
        }
        setDeletedUrls(
          _.intersection(initialValues.environmentUrls, values.environmentUrls)
            .length < initialValues.environmentUrls.length
        );

        return (
          <Form>
            <React.Fragment>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t("group.scope.git.envUrls")}
              </ControlLabel>
              <FormikArrayField
                allowEmpty={true}
                initialValue={""}
                name={"environmentUrls"}
              >
                {(fieldName: string): JSX.Element => (
                  <Field
                    component={FormikText}
                    name={fieldName}
                    type={"text"}
                  />
                )}
              </FormikArrayField>
              <div>
                {!showAlert && modalMessages.message !== "" && (
                  <Alert
                    icon={true}
                    timer={setShowAlert}
                    variant={modalMessages.type as IAlertProps["variant"]}
                  >
                    {modalMessages.message}
                  </Alert>
                )}
              </div>
              {deletedUrls ? (
                <FormGroup>
                  <br />
                  <ControlLabel>
                    <RequiredField>{"*"}&nbsp;</RequiredField>
                    {t("group.scope.common.deactivation.reason.verboseLabel")}
                  </ControlLabel>
                  <Field component={FormikDropdown} name={"reason"}>
                    <option value={""} />
                    <option value={"OUT_OF_SCOPE"}>
                      {t("group.scope.common.deactivation.reason.scope")}
                    </option>
                    <option value={"REGISTERED_BY_MISTAKE"}>
                      {t("group.scope.common.deactivation.reason.mistake")}
                    </option>
                    <option value={"OTHER"}>
                      {t("group.scope.common.deactivation.reason.other")}
                    </option>
                  </Field>
                </FormGroup>
              ) : undefined}
              {deletedUrls && values.reason === "OTHER" ? (
                <FormGroup>
                  <ControlLabel>
                    <RequiredField>{"*"}&nbsp;</RequiredField>
                    {t("group.scope.common.deactivation.other")}
                  </ControlLabel>
                  <Field component={FormikText} name={"other"} />
                </FormGroup>
              ) : undefined}
              <ModalFooter>
                <Button onClick={onClose} variant={"secondary"}>
                  {t("confirmmodal.cancel")}
                </Button>
                <Button
                  disabled={!dirty || isSubmitting}
                  id={"envs-manage-proceed"}
                  type={"submit"}
                  variant={"primary"}
                >
                  {t("confirmmodal.proceed")}
                </Button>
              </ModalFooter>
            </React.Fragment>
          </Form>
        );
      }}
    </Formik>
  );
};

export { Environments };
