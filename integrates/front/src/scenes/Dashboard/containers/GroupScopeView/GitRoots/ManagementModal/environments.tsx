import { Field, Form, Formik } from "formik";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { array, object, string } from "yup";

import type { IGitRootAttr } from "../../types";
import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Button } from "components/Button";
import { ModalFooter } from "components/Modal";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikArrayField, FormikText } from "utils/forms/fields";

interface IEnvironmentsProps {
  initialValues: IGitRootAttr;
  modalMessages: { message: string; type: string };
  onClose: () => void;
  onSubmit: (values: IGitRootAttr) => Promise<void>;
}

const Environments: React.FC<IEnvironmentsProps> = ({
  initialValues,
  modalMessages,
  onClose,
  onSubmit,
}: IEnvironmentsProps): JSX.Element => {
  const { t } = useTranslation();
  const validations = object().shape({
    environmentUrls: array().of(string().required(t("validations.required"))),
  });

  const [showAlert, setShowAlert] = useState(false);

  return (
    <Formik
      initialValues={initialValues}
      name={"gitEnvs"}
      onSubmit={onSubmit}
      validationSchema={validations}
    >
      {({ dirty, isSubmitting }): JSX.Element => {
        if (isSubmitting) {
          setShowAlert(false);
        }

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
