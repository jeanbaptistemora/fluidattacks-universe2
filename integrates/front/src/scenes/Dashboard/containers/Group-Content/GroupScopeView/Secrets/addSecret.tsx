import { useMutation } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Form, Formik } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { lazy, object, string } from "yup";
import type { BaseSchema } from "yup";

import { ADD_SECRET, REMOVE_SECRET } from "../queries";
import { Button } from "components/Button";
import type { IConfirmFn } from "components/ConfirmDialog";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Input, TextArea } from "components/Input";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { translate } from "utils/translations/translate";

interface ISecretsProps {
  groupName: string;
  isUpdate: boolean;
  secretDescription: string;
  secretKey: string;
  rootId: string;
  secretValue: string;
  setModalMessages: React.Dispatch<
    React.SetStateAction<{
      message: string;
      type: string;
    }>
  >;
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
  secretDescription,
  secretKey,
  rootId,
  secretValue,
  setModalMessages,
  closeModal,
  isDuplicated,
  handleSubmitSecret,
}: ISecretsProps): JSX.Element => {
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canAddSecret: boolean = permissions.can(
    "api_mutations_add_secret_mutate"
  );
  const canRemoveSecret: boolean = permissions.can(
    "api_mutations_remove_secret_mutate"
  );
  const initialValues = {
    description: secretDescription,
    key: secretKey,
    value: secretValue,
  };

  const { t } = useTranslation();
  const [addSecret] = useMutation(ADD_SECRET, {
    onCompleted: (): void => {
      setModalMessages({
        message: t("group.scope.git.repo.credentials.secrets.success"),
        type: "success",
      });
      handleSubmitSecret();
      closeModal();
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        setModalMessages({
          message: t("groupAlerts.errorTextsad"),
          type: "error",
        });
        Logger.error("Couldn't add url roots", error);
      });
    },
  });

  const [removeSecret] = useMutation(REMOVE_SECRET, {
    onCompleted: (): void => {
      setModalMessages({
        message: t("group.scope.git.repo.credentials.secrets.removed"),
        type: "success",
      });
      handleSubmitSecret();
      closeModal();
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        setModalMessages({
          message: t("groupAlerts.errorTextsad"),
          type: "error",
        });
        Logger.error("Couldn't add url roots", error);
      });
    },
  });

  const handleSecretSubmit = useCallback(
    async ({
      description,
      key,
      value,
    }: {
      description: string;
      key: string;
      value: string;
    }): Promise<void> => {
      await addSecret({
        variables: { description, groupName, key, rootId, value },
      });
    },
    [addSecret, groupName, rootId]
  );

  const handleRemoveClick = useCallback((): void => {
    void removeSecret({ variables: { groupName, key: secretKey, rootId } });
  }, [groupName, removeSecret, rootId, secretKey]);

  const onConfirmDelete = useCallback(
    (confirm: IConfirmFn): (() => void) =>
      (): void => {
        confirm((): void => {
          handleRemoveClick();
        });
      },
    [handleRemoveClick]
  );

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
                  <Input disabled={isUpdate} name={"key"} type={"text"} />
                </div>
                <div className={"mt3"}>
                  <TextArea
                    label={t("group.scope.git.repo.credentials.secrets.value")}
                    name={"value"}
                    required={true}
                  />
                </div>
                <div className={"mt3"}>
                  <TextArea
                    label={t(
                      "group.scope.git.repo.credentials.secrets.description"
                    )}
                    name={"description"}
                  />
                </div>
                <div className={"mt3"}>
                  <Button
                    disabled={
                      !isValid || !dirty || isSubmitting || !canAddSecret
                    }
                    id={"git-root-add-secret"}
                    type={"submit"}
                    variant={"primary"}
                  >
                    {t("components.modal.confirm")}
                  </Button>
                  {isUpdate && canRemoveSecret ? (
                    <ConfirmDialog
                      title={t(
                        "group.scope.git.repo.credentials.secrets.remove"
                      )}
                    >
                      {(confirm): JSX.Element => {
                        return (
                          <Button
                            id={"git-root-remove-secret"}
                            onClick={onConfirmDelete(confirm)}
                            variant={"secondary"}
                          >
                            <FontAwesomeIcon icon={faTrashAlt} />
                          </Button>
                        );
                      }}
                    </ConfirmDialog>
                  ) : undefined}
                  <Button
                    id={"git-root-add-secret-cancel"}
                    onClick={closeModal}
                    variant={"secondary"}
                  >
                    {t("components.modal.cancel")}
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
