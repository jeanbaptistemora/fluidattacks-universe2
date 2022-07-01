import { Buffer } from "buffer";

import type { ApolloError, FetchResult } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import type { FormikHelpers } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { ActionButtons } from "./ActionButtons";
import { CredentialsForm } from "./CredentialsForm";
import type { IFormValues } from "./CredentialsForm/types";
import {
  ADD_CREDENTIALS,
  GET_STAKEHOLDER_CREDENTIALS,
  GET_STAKEHOLDER_ORGANIZATIONS,
  REMOVE_CREDENTIALS,
  UPDATE_CREDENTIALS,
} from "./queries";
import type {
  IAddCredentialsResultAttr,
  ICredentialAttr,
  ICredentialData,
  ICredentialModalProps as ICredentialsModalProps,
  IOrganizationAttr,
  IRemoveCredentialsResultAttr,
  IUpdateCredentialsResultAttr,
} from "./types";
import { getCredentialsIndex, onSelectSeveralCredentialsHelper } from "./utils";

import { Modal } from "components/Modal";
import { Table } from "components/Table";
import type { IHeaderConfig, ISelectRowProps } from "components/Table/types";
import { filterSearchText } from "components/Table/utils/filters";
import { editAndDeleteActionFormatter } from "scenes/Dashboard/components/Navbar/UserProfile/CredentialsModal/formatters/editAndDeleteActionFormatter";
import { GET_ROOTS } from "scenes/Dashboard/containers/GroupScopeView/queries";
import { getErrors } from "utils/helpers";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const CredentialsModal: React.FC<ICredentialsModalProps> = (
  props: ICredentialsModalProps
): JSX.Element => {
  const { onClose } = props;
  const { t } = useTranslation();

  // States
  const [isAdding, setIsAdding] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [isEditingSecrets, setIsEditingSecrets] = useState(false);
  const [credentialsToEditId, setCredentialsToEditId] = useState<
    string | undefined
  >(undefined);
  const [formInitialValues, setFormInitialValues] = useState<
    IFormValues | undefined
  >(undefined);
  const [newSecrets, setNewSecrets] = useState(false);
  const [selectedCredentialsDatas, setSelectedCredentialsDatas] = useState<
    ICredentialData[]
  >([]);
  const [searchTextFilter, setSearchTextFilter] = useState("");

  // GraphQl mutations
  const [handleAddCredentials] = useMutation<IAddCredentialsResultAttr>(
    ADD_CREDENTIALS,
    {
      onCompleted: (data: IAddCredentialsResultAttr): void => {
        if (data.addCredentials.success) {
          msgSuccess(
            t("profile.credentialsModal.alerts.addSuccess"),
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
      refetchQueries: [GET_STAKEHOLDER_CREDENTIALS],
    }
  );
  const [handleRemoveCredentials] = useMutation<IRemoveCredentialsResultAttr>(
    REMOVE_CREDENTIALS,
    {
      onCompleted: (data: IRemoveCredentialsResultAttr): void => {
        if (data.removeCredentials.success) {
          msgSuccess(
            t("profile.credentialsModal.alerts.removeSuccess"),
            t("groupAlerts.titleSuccess")
          );
        }
      },
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred adding credentials", error);
          }
        });
      },
      refetchQueries: [GET_STAKEHOLDER_CREDENTIALS, GET_ROOTS],
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

  // GraphQl queries
  const { data, refetch: refetchStakeholderCredentials } = useQuery<{
    me: { credentials: ICredentialAttr[] };
  }>(GET_STAKEHOLDER_CREDENTIALS, {
    onCompleted: ({
      me: { credentials },
    }: {
      me: { credentials: ICredentialAttr[] };
    }): void => {
      if (credentials.length === 0) {
        setIsAdding(true);
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load stakeholder credentials", error);
      });
    },
  });
  const { data: organizationsData } = useQuery<{
    me: { organizations: IOrganizationAttr[] };
  }>(GET_STAKEHOLDER_ORGANIZATIONS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load stakeholder credentials", error);
      });
    },
  });

  // Format data
  const credentialsAttrs = _.isUndefined(data) ? [] : data.me.credentials;
  const credentials: ICredentialData[] = credentialsAttrs.map(
    (credentialAttr: ICredentialAttr): ICredentialData => ({
      ...credentialAttr,
      organizationId: credentialAttr.organization.id,
      organizationName: credentialAttr.organization.name,
    })
  );

  const organizations = _.isUndefined(organizationsData)
    ? []
    : organizationsData.me.organizations;

  // Handle responses
  const handleOnEditCompleted = (
    result: FetchResult<IUpdateCredentialsResultAttr>,
    resetForm: () => void
  ): void => {
    if (!_.isNil(result.data) && result.data.updateCredentials.success) {
      msgSuccess(
        t("profile.credentialsModal.alerts.editSuccess"),
        t("groupAlerts.titleSuccess")
      );
      setSelectedCredentialsDatas([]);
      void refetchStakeholderCredentials();
      resetForm();
      setIsEditing(false);
      setIsEditingSecrets(false);
    }
  };

  // Handle actions
  async function handleSubmit(
    values: IFormValues,
    { resetForm }: FormikHelpers<IFormValues>
  ): Promise<void> {
    const secrets = values.isHttpsType
      ? values.isHttpsPasswordType
        ? {
            password: values.password,
            type: "HTTPS",
            user: values.user,
          }
        : { token: values.accessToken, type: "HTTPS" }
      : {
          key: Buffer.from(
            _.isUndefined(values.sshKey) ? "" : values.sshKey
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
          organizationId: values.organization,
        },
      });
      if (
        !_.isNil(addingResult.data) &&
        addingResult.data.addCredentials.success
      ) {
        resetForm();
        setIsAdding(false);
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
          credentialsId: credentialsToEditId,
          organizationId: values.organization,
        },
      });
      const errors = getErrors<IUpdateCredentialsResultAttr>([editingResult]);

      if (_.isEmpty(errors)) {
        handleOnEditCompleted(editingResult, resetForm);
      } else {
        void refetchStakeholderCredentials();
      }
    }
    if (isEditingSecrets) {
      const results = await Promise.all(
        selectedCredentialsDatas.map(
          async (
            selectedCredentialsData: ICredentialData
          ): Promise<FetchResult<IUpdateCredentialsResultAttr>> =>
            handleUpdateCredentials({
              variables: {
                credentials: secrets,
                credentialsId: selectedCredentialsData.id,
                organizationId: selectedCredentialsData.organizationId,
              },
            })
        )
      );
      const errors = getErrors<IUpdateCredentialsResultAttr>(results);

      if (!_.isEmpty(results) && _.isEmpty(errors)) {
        handleOnEditCompleted(results[0], resetForm);
      } else {
        void refetchStakeholderCredentials();
      }
    }
  }
  function handleOnAdd(): void {
    setIsAdding(true);
  }
  function handleOnCancel(): void {
    setIsAdding(false);
    setIsEditing(false);
    setIsEditingSecrets(false);
  }
  function handleOnEditSecrets(): void {
    setIsEditingSecrets(true);
  }
  function handleOnRemove(
    credentialsToRemove: Record<string, string> | undefined
  ): void {
    if (!_.isUndefined(credentialsToRemove)) {
      void handleRemoveCredentials({
        variables: {
          credentialsId: credentialsToRemove.id,
          organizationId: credentialsToRemove.organizationId,
        },
      });
    }
  }
  function handleOnEdit(
    credentialsToEdit: Record<string, string> | undefined
  ): void {
    if (!_.isUndefined(credentialsToEdit)) {
      setFormInitialValues({
        accessToken: undefined,
        isHttpsPasswordType: true,
        isHttpsType: credentialsToEdit.type === "HTTPS",
        name: credentialsToEdit.name,
        organization: credentialsToEdit.organizationId,
        password: undefined,
        sshKey: undefined,
        user: undefined,
      });
      setCredentialsToEditId(credentialsToEdit.id);
      setIsEditing(true);
      setIsAdding(false);
    }
  }
  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }

  // Filter data
  const filteredCredentials: ICredentialData[] = filterSearchText(
    credentials,
    searchTextFilter
  );

  // Table config
  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "name",
      header: t("profile.credentialsModal.table.columns.name"),
      wrapped: true,
    },
    {
      dataField: "type",
      header: t("profile.credentialsModal.table.columns.type"),
      wrapped: true,
    },
    {
      dataField: "organizationName",
      header: t("profile.credentialsModal.table.columns.organization"),
      wrapped: true,
    },
    {
      dataField: "id",
      deleteFunction: handleOnRemove,
      editFunction: handleOnEdit,
      formatter: editAndDeleteActionFormatter,
      header: t("profile.credentialsModal.table.columns.action"),
      omit: isEditingSecrets,
      width: "60px",
    },
  ];
  function onSelectSeveralCredentials(
    isSelect: boolean,
    credentialDatasSelected: ICredentialData[]
  ): string[] {
    return onSelectSeveralCredentialsHelper(
      isSelect,
      credentialDatasSelected,
      selectedCredentialsDatas,
      setSelectedCredentialsDatas
    );
  }
  function onSelectOneCredentials(
    credentialsData: ICredentialData,
    isSelect: boolean
  ): boolean {
    onSelectSeveralCredentials(isSelect, [credentialsData]);

    return true;
  }

  const selectionMode: ISelectRowProps = {
    clickToSelect: false,
    hideSelectColumn: !isEditingSecrets,
    mode: "checkbox",
    nonSelectable: undefined,
    onSelect: onSelectOneCredentials,
    onSelectAll: onSelectSeveralCredentials,
    selected: getCredentialsIndex(
      selectedCredentialsDatas,
      filteredCredentials
    ),
  };

  return (
    <Modal
      minWidth={850}
      onClose={onClose}
      open={true}
      title={t("profile.credentialsModal.title")}
    >
      <CredentialsForm
        areSelectedCredentials={selectedCredentialsDatas.length > 0}
        initialValues={isAdding ? undefined : formInitialValues}
        isAdding={isAdding}
        isEditing={isEditing}
        isEditingSecrets={isEditingSecrets}
        newSecrets={newSecrets}
        onCancel={handleOnCancel}
        onSubmit={handleSubmit}
        organizations={organizations}
        setNewSecrets={setNewSecrets}
      />
      {isAdding || isEditing ? undefined : (
        <Table
          customSearch={{
            customSearchDefault: searchTextFilter,
            isCustomSearchEnabled: true,
            onUpdateCustomSearch: onSearchTextChange,
            position: isEditingSecrets ? "right" : "left",
          }}
          dataset={filteredCredentials}
          exportCsv={false}
          extraButtonsRight={
            <ActionButtons
              isAdding={isAdding}
              isEditingSecrets={isEditingSecrets}
              onAdd={handleOnAdd}
              onEditSecrets={handleOnEditSecrets}
            />
          }
          headers={tableHeaders}
          id={"tblCredentials"}
          pageSize={10}
          search={false}
          selectionMode={selectionMode}
        />
      )}
    </Modal>
  );
};

export { CredentialsModal };
