/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { Buffer } from "buffer";

import type { ApolloError } from "@apollo/client";
import { useMutation } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { CredentialsForm } from "./CredentialsForm";
import type { IFormValues } from "./CredentialsForm/types";
import type { ICredentialsModalProps } from "./types";

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

  // Handle actions
  async function handleSubmit(values: IFormValues): Promise<void> {
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
                auth: "TOKEN",
                key: undefined,
                name: selectedCredentials[0].name,
                newSecrets: false,
                password: undefined,
                token: undefined,
                type: selectedCredentials[0].type,
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
