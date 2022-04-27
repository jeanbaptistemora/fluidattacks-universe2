import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
import React, { useCallback, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import { AddSecret } from "./addSecret";

import { GET_ENVIRONMENT_URL } from "../../queries";
import type { IEnvironmentUrl, ISecret } from "../../types";
import { renderSecretsDescription } from "../ManagementModal/secretDescription";
import { SecretValue } from "../ManagementModal/secretValue";
import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { Table } from "components/Table";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";

interface ISecretItem {
  description: string;
  element: JSX.Element;
  key: string;
  value: string;
}

interface IManagementModalProps {
  closeModal: () => void;
  urlId: string;
  groupName: string;
  isOpen: boolean;
}
const ManagementEnvironmentUrlsModal: React.FC<IManagementModalProps> = ({
  groupName,
  isOpen,
  closeModal,
  urlId,
}: IManagementModalProps): JSX.Element => {
  const { t } = useTranslation();

  const defaultCurrentRow: ISecret = useMemo((): ISecret => {
    return { description: "", key: "", value: "" };
  }, []);
  const [currentRow, setCurrentRow] = useState(defaultCurrentRow);
  const [isUpdate, setIsUpdate] = useState(false);

  const [addSecretModalOpen, setAddSecretModalOpen] = useState(false);
  const { data, refetch } = useQuery<{ environmentUrl: IEnvironmentUrl }>(
    GET_ENVIRONMENT_URL,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load secrets", error);
        });
      },
      variables: { groupName, urlId },
    }
  );
  function editCurrentRow(
    key: string,
    value: string,
    description: string
  ): void {
    setCurrentRow({ description, key, value });
    setIsUpdate(true);
    setAddSecretModalOpen(true);
  }

  const secretsDataSet =
    data === undefined
      ? []
      : data.environmentUrl.secrets.map((item: ISecret): ISecretItem => {
          return {
            description: item.description,
            element: (
              <SecretValue
                onEdit={editCurrentRow}
                secretDescription={item.description}
                secretKey={item.key}
                secretValue={item.value}
              />
            ),
            key: item.key,
            value: item.value,
          };
        });
  function closeAddModal(): void {
    setIsUpdate(false);
    setCurrentRow(defaultCurrentRow);
    setAddSecretModalOpen(false);
  }
  function openModal(): void {
    setAddSecretModalOpen(true);
  }
  function isSecretDuplicated(key: string): boolean {
    return secretsDataSet.some((item): boolean => item.key === key);
  }
  const onCloseModal: () => void = useCallback((): void => {
    closeModal();
    setIsUpdate(false);
    setCurrentRow(defaultCurrentRow);
    setAddSecretModalOpen(false);
  }, [closeModal, defaultCurrentRow]);

  return (
    <React.StrictMode>
      <Modal onClose={onCloseModal} open={isOpen} title={"Secrets"}>
        <Modal
          open={addSecretModalOpen}
          title={t("group.scope.git.repo.credentials.secrets.tittle")}
        >
          <AddSecret
            closeModal={closeAddModal}
            groupName={groupName}
            handleSubmitSecret={refetch}
            isDuplicated={isSecretDuplicated}
            isUpdate={isUpdate}
            secretDescription={currentRow.description}
            secretKey={currentRow.key}
            secretValue={currentRow.value}
            urlId={urlId}
          />
        </Modal>
        <Table
          dataset={secretsDataSet}
          expandRow={{
            expandByColumnOnly: true,
            renderer: renderSecretsDescription,
            showExpandColumn: true,
          }}
          exportCsv={false}
          headers={[
            {
              dataField: "key",
              header: t("group.scope.git.repo.credentials.secrets.key"),
            },
            {
              dataField: "element",
              header: t("group.scope.git.repo.credentials.secrets.value"),
            },
          ]}
          id={"tblGitRootSecrets"}
          pageSize={10}
          search={false}
        />
        <Can do={"api_mutations_add_git_environment_secret_mutate"}>
          <Button id={"add-secret"} onClick={openModal} variant={"secondary"}>
            {"Add secret"}
          </Button>
        </Can>
      </Modal>
    </React.StrictMode>
  );
};

export { ManagementEnvironmentUrlsModal };
