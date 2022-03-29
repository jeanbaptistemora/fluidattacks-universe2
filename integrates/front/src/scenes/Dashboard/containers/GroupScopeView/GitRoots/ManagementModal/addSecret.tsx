import { useMutation } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { lazy, object, string } from "yup";
import type { BaseSchema } from "yup";

import { ADD_SECRET } from "../../queries";
import { Button } from "components/Button";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikText, FormikTextArea } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface ISecretsProps {
  groupName: string;
  key: string;
  rootId: string;
  value: string;
  closeModal: () => void;
}

const secretSchema = lazy(
  (): BaseSchema =>
    object().shape({
      secretKey: string()
        .required(translate.t("validations.required"))
        .matches(/^[a-zA-Z_0-9-]{1,128}$/u),
      secretValue: string().required(translate.t("validations.required")),
    })
);

const AddSecret: React.FC<ISecretsProps> = ({
  groupName,
  key,
  rootId,
  value,
  closeModal,
}: ISecretsProps): JSX.Element => {
  const initialValues = { secretKey: key, secretValue: value };
  const { t } = useTranslation();
  const [addSecret] = useMutation(ADD_SECRET, {
    onCompleted: (): void => {
      msgSuccess(
        t("group.scope.git.repo.credentials.secrets.success"),
        t("group.scope.git.repo.credentials.secrets.successTitle")
      );
      closeModal();
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.error("Couldn't add url roots", error);
      });
    },
  });
  const handleSecretSubmit = useCallback(
    async ({
      secretKey,
      secretValue,
    }: {
      secretKey: string;
      secretValue: string;
    }): Promise<void> => {
      await addSecret({
        variables: { groupName, key: secretKey, rootId, value: secretValue },
      });
    },
    [addSecret, groupName, rootId]
  );

  return (
    <div>
      <Formik
        initialValues={initialValues}
        name={"gitRootSecret"}
        onSubmit={handleSecretSubmit}
        validationSchema={secretSchema}
      >
        {(): JSX.Element => (
          <Form>
            <fieldset className={"bn"}>
              <legend className={"f3 b"}>
                {_.isUndefined(key) || key.length === 0
                  ? t("group.scope.git.repo.credentials.secrets.add")
                  : t("group.scope.git.repo.credentials.secrets.update")}
              </legend>
              <div>
                <div>
                  <ControlLabel>
                    <RequiredField>{"*"}&nbsp;</RequiredField>
                    {"Key"}
                  </ControlLabel>
                  <Field
                    component={FormikText}
                    name={"secretKey"}
                    type={"text"}
                  />
                </div>
                <div className={"mt3"}>
                  <ControlLabel>
                    <RequiredField>{"*"}&nbsp;</RequiredField>
                    {"Value"}
                  </ControlLabel>
                  <Field
                    component={FormikTextArea}
                    name={"secretValue"}
                    type={"text"}
                  />
                </div>
                <div className={"mt3"}>
                  <Button
                    id={"git-root-add-secret"}
                    type={"submit"}
                    variant={"primary"}
                  >
                    {t("confirmmodal.proceed")}
                  </Button>
                  <Button
                    id={"git-root-add-secret-cancel"}
                    onClick={closeModal}
                    variant={"secondary"}
                  >
                    {t("confirmmodal.cancel")}
                  </Button>
                </div>
              </div>
            </fieldset>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export { AddSecret };
