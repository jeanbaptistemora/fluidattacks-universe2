import { Buffer } from "buffer";

import type { ApolloError } from "@apollo/client";
import { useMutation } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { CredentialsForm } from "./CredentialsForm";
import type { IFormValues } from "./CredentialsForm/types";
import type { ICredentialsModalProps, ISecretsCredentials } from "./types";

import {
  ADD_CREDENTIALS,
  GET_ORGANIZATION_CREDENTIALS,
  UPDATE_CREDENTIALS,
} from "../queries";
import type {
  IAddCredentialsResultAttr,
  IUpdateCredentialsResultAttr,
} from "../types";
import { Modal } from "components/Modal";
import {
  formatAuthCredentials,
  formatTypeCredentials,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/utils";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const CredentialsModal: React.FC<ICredentialsModalProps> = (
  props: ICredentialsModalProps
): JSX.Element => {
  const {
    isAdding,
    isEditing,
    organizationId,
    onClose,
    selectedCredentials,
    setSelectedCredentials,
  } = props;
  const { t } = useTranslation();

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
          onClose();
          setSelectedCredentials([]);
        }
      },
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - A credential exists with the same name":
              msgError(t("validations.invalidCredentialName"));
              break;
            case "Exception - Field cannot fill with blank characters":
              msgError(t("validations.invalidSpaceField"));
              break;
            case "Exception - Password should start with a letter":
              msgError(t("validations.credentialsModal.startWithLetter"));
              break;
            case "Exception - Password should include at least one number":
              msgError(t("validations.credentialsModal.includeNumber"));
              break;
            case "Exception - Password should include lowercase characters":
              msgError(t("validations.credentialsModal.includeLowercase"));
              break;
            case "Exception - Password should include uppercase characters":
              msgError(t("validations.credentialsModal.includeUppercase"));
              break;
            case "Exception - Password should include symbols characters":
              msgError(t("validations.credentialsModal.includeSymbols"));
              break;
            case "Exception - Password should not include sequentials characters":
              msgError(t("validations.credentialsModal.sequentialsCharacters"));
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
      onCompleted: (data: IUpdateCredentialsResultAttr): void => {
        if (data.updateCredentials.success) {
          msgSuccess(
            t("organization.tabs.credentials.alerts.editSuccess"),
            t("groupAlerts.titleSuccess")
          );
          onClose();
          setSelectedCredentials([]);
        }
      },
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - A credential exists with the same name":
              msgError(t("validations.invalidCredentialName"));
              break;
            case "Exception - Field cannot fill with blank characters":
              msgError(t("validations.invalidSpaceField"));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred editing credentials", error);
          }
        });
      },
      refetchQueries: [GET_ORGANIZATION_CREDENTIALS],
    }
  );

  const formatSecrets = useCallback(
    (values: IFormValues): ISecretsCredentials => {
      if (values.type === "HTTPS") {
        if (values.auth === "USER") {
          return {
            password: values.password,
            type: "HTTPS",
            user: values.user,
          };
        }

        return {
          azureOrganization:
            _.isUndefined(values.azureOrganization) ||
            _.isUndefined(values.isPat) ||
            !values.isPat
              ? undefined
              : values.azureOrganization,
          isPat: _.isUndefined(values.isPat) ? false : values.isPat,
          token: values.token,
          type: "HTTPS",
        };
      }

      return {
        key: Buffer.from(_.isUndefined(values.key) ? "" : values.key).toString(
          "base64"
        ),
        type: "SSH",
      };
    },
    []
  );

  // Handle actions
  async function handleSubmit(values: IFormValues): Promise<void> {
    const secrets = formatSecrets(values);

    if (isAdding) {
      await handleAddCredentials({
        variables: {
          credentials: {
            name: values.name,
            ...secrets,
          },
          organizationId,
        },
      });
    }

    if (isEditing && !_.isUndefined(selectedCredentials)) {
      await handleUpdateCredentials({
        variables: {
          credentials: values.newSecrets
            ? {
                name: values.name,
                ...secrets,
              }
            : {
                name: values.name,
              },
          credentialsId: selectedCredentials[0].id,
          organizationId,
        },
      });
    }
  }

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t("profile.credentialsModal.title")}
    >
      <CredentialsForm
        initialValues={
          isEditing && !_.isUndefined(selectedCredentials)
            ? {
                auth: formatAuthCredentials(selectedCredentials[0]),
                azureOrganization:
                  selectedCredentials[0].azureOrganization ?? "",
                isPat: selectedCredentials[0].isPat,
                key: undefined,
                name: selectedCredentials[0].name,
                newSecrets: false,
                password: undefined,
                token: undefined,
                type: selectedCredentials[0].type,
                typeCredential: formatTypeCredentials(selectedCredentials[0]),
                user: undefined,
              }
            : undefined
        }
        isAdding={isAdding}
        isEditing={isEditing}
        onCancel={onClose}
        onSubmit={handleSubmit}
      />
    </Modal>
  );
};

export { CredentialsModal };
