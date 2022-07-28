import { Buffer } from "buffer";

import type { ApolloError, FetchResult } from "@apollo/client";
import { useMutation } from "@apollo/client";
import type { FormikHelpers } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { CredentialsForm } from "./CredentialsForm";
import type { IFormValues } from "./CredentialsForm/types";
import type {
  IAddCredentialsResultAttr,
  ICredentialModalProps as ICredentialsModalProps,
  IUpdateCredentialsResultAttr,
} from "./types";

import {
  ADD_CREDENTIALS,
  GET_ORGANIZATION_CREDENTIALS,
  UPDATE_CREDENTIALS,
} from "../queries";
import { Modal } from "components/Modal";
import { getErrors } from "utils/helpers";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const CredentialsModal: React.FC<ICredentialsModalProps> = (
  props: ICredentialsModalProps
): JSX.Element => {
  const { isAdding, isEditing, organizationId, onClose } = props;
  const { t } = useTranslation();

  // States
  const [newSecrets, setNewSecrets] = useState(false);

  // GraphQl mutations
  const [handleAddCredentials] = useMutation<IAddCredentialsResultAttr>(
    ADD_CREDENTIALS,
    {
      onCompleted: (data: IAddCredentialsResultAttr): void => {
        if (data.addCredentials.success) {
          msgSuccess(
            t("organization.tabs.credentials.alerts.addSuccess"),
            t("groupAlerts.titleSuccess")
          );
        }
      },
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - A credential exists with the same name":
              msgError(t("validations.invalidCredentialName"));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred adding credential", error);
          }
        });
      },
      refetchQueries: [GET_ORGANIZATION_CREDENTIALS],
    }
  );
  const [handleUpdateCredentials] = useMutation<IUpdateCredentialsResultAttr>(
    UPDATE_CREDENTIALS,
    {
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - A credential exists with the same name":
              msgError(t("validations.invalidCredentialName"));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred editing credentials", error);
          }
        });
      },
    }
  );

  // Handle responses
  const handleOnEditCompleted = (
    result: FetchResult<IUpdateCredentialsResultAttr>,
    resetForm: () => void
  ): void => {
    if (!_.isNil(result.data) && result.data.updateCredentials.success) {
      msgSuccess(
        t("organization.tabs.credentials.alerts.editSuccess"),
        t("groupAlerts.titleSuccess")
      );
      resetForm();
      onClose();
    }
  };

  // Handle actions
  async function handleSubmit(
    values: IFormValues,
    { resetForm }: FormikHelpers<IFormValues>
  ): Promise<void> {
    const secrets =
      values.type === "HTTPS"
        ? values.auth === "USER"
          ? {
              password: values.password,
              type: "HTTPS",
              user: values.user,
            }
          : { token: values.token, type: "HTTPS" }
        : {
            key: Buffer.from(
              _.isUndefined(values.key) ? "" : values.key
            ).toString("base64"),
            type: "SSH",
          };

    if (isAdding) {
      const addingResult = await handleAddCredentials({
        variables: {
          credentials: {
            name: values.name,
            ...secrets,
          },
          organizationId,
        },
      });
      if (
        !_.isNil(addingResult.data) &&
        addingResult.data.addCredentials.success
      ) {
        resetForm();
        onClose();
      }
    }

    if (isEditing) {
      const editingResult = await handleUpdateCredentials({
        variables: {
          credentials: newSecrets
            ? {
                name: values.name,
                ...secrets,
              }
            : {
                name: values.name,
              },
          // CredentialsId: credentialsToEditId,
          organizationId: values,
        },
      });
      const errors = getErrors<IUpdateCredentialsResultAttr>([editingResult]);

      if (_.isEmpty(errors)) {
        handleOnEditCompleted(editingResult, resetForm);
      }
    }
  }

  return (
    <Modal
      minWidth={850}
      onClose={onClose}
      open={true}
      title={t("profile.credentialsModal.title")}
    >
      <CredentialsForm
        initialValues={undefined}
        isAdding={isAdding}
        newSecrets={newSecrets}
        onCancel={onClose}
        onSubmit={handleSubmit}
        setNewSecrets={setNewSecrets}
      />
    </Modal>
  );
};

export { CredentialsModal };
