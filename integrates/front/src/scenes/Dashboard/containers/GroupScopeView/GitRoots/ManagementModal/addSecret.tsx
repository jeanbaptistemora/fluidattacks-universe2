import { useMutation } from "@apollo/client";
import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { lazy, object, string } from "yup";
import type { BaseSchema } from "yup";

import { ADD_SECRET, REMOVE_SECRET } from "../../queries";
import { Button } from "components/Button";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikText, FormikTextArea } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface ISecretsProps {
  groupName: string;
  isUpdate: boolean;
  secretKey: string;
  rootId: string;
  secretValue: string;
  closeModal: () => void;
  handleSubmitSecret: () => void;
  isDuplicated: (key: string) => boolean;
}

function getSecretSchema(
  duplicateValidator: (key: string) => boolean,
  isUpdate: boolean = false
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
): any {
  return lazy(
    (): BaseSchema =>
      object().shape({
        key: string()
          .required(translate.t("validations.required"))
          .matches(/^[a-zA-Z_0-9-]{1,128}$/u)
          .test(
            "duplicateValue",
            translate.t("validations.duplicateSecret"),
            (value): boolean => {
              if (_.isUndefined(value) || isUpdate) {
                return true;
              }

              return !duplicateValidator(value);
            }
          ),
        value: string().required(translate.t("validations.required")),
      })
  );
}

const AddSecret: React.FC<ISecretsProps> = ({
  groupName,
  isUpdate,
  secretKey,
  rootId,
  secretValue,
  closeModal,
  isDuplicated,
  handleSubmitSecret,
}: ISecretsProps): JSX.Element => {
  const initialValues = { key: secretKey, value: secretValue };

  const { t } = useTranslation();
  const [addSecret] = useMutation(ADD_SECRET, {
    onCompleted: (): void => {
      msgSuccess(
        t("group.scope.git.repo.credentials.secrets.success"),
        t("group.scope.git.repo.credentials.secrets.successTitle")
      );
      handleSubmitSecret();
      closeModal();
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.error("Couldn't add url roots", error);
      });
    },
  });

  const [removeSecret] = useMutation(REMOVE_SECRET, {
    onCompleted: (): void => {
      msgSuccess(
        t("group.scope.git.repo.credentials.secrets.removed"),
        t("group.scope.git.repo.credentials.secrets.successTitle")
      );
      handleSubmitSecret();
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
    async ({ key, value }: { key: string; value: string }): Promise<void> => {
      await addSecret({
        variables: { groupName, key, rootId, value },
      });
    },
    [addSecret, groupName, rootId]
  );

  function handleRemoveClick(): void {
    void removeSecret({ variables: { key: secretKey, rootId } });
  }

  return (
    <div>
      <Formik
        initialValues={initialValues}
        name={"gitRootSecret"}
        onSubmit={handleSecretSubmit}
        validationSchema={getSecretSchema(isDuplicated, isUpdate)}
      >
        {({ isValid, dirty, isSubmitting }): JSX.Element => (
          <Form>
            <fieldset className={"bn"}>
              <legend className={"f3 b"}>
                {isUpdate
                  ? t("group.scope.git.repo.credentials.secrets.update")
                  : t("group.scope.git.repo.credentials.secrets.add")}
              </legend>
              <div>
                <div>
                  <ControlLabel>
                    <RequiredField>{"*"}&nbsp;</RequiredField>
                    {"Key"}
                  </ControlLabel>
                  <Field component={FormikText} name={"key"} type={"text"} />
                </div>
                <div className={"mt3"}>
                  <ControlLabel>
                    <RequiredField>{"*"}&nbsp;</RequiredField>
                    {"Value"}
                  </ControlLabel>
                  <Field
                    component={FormikTextArea}
                    name={"value"}
                    type={"text"}
                  />
                </div>
                <div className={"mt3"}>
                  <Button
                    disabled={!isValid || !dirty || isSubmitting}
                    id={"git-root-add-secret"}
                    type={"submit"}
                    variant={"primary"}
                  >
                    {t("confirmmodal.proceed")}
                  </Button>
                  {isUpdate ? (
                    <Button
                      id={"git-root-remove-secret"}
                      onClick={handleRemoveClick}
                      variant={"secondary"}
                    >
                      <FontAwesomeIcon icon={faTrashAlt} />
                    </Button>
                  ) : undefined}
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
