import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { AddSecret } from "./addSecret";
import { SecretValue } from "./secretValue";

import { GET_ROOT } from "../../queries";
import type { IGitRootAttr } from "../../types";
import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { Table } from "components/Table";
import { Logger } from "utils/logger";

interface ISecret {
  description: string;
  key: string;
  value: string;
}
interface ISecretItem {
  description: string;
  element: JSX.Element;
  key: string;
  value: string;
}

interface ISecretsProps {
  gitRootId: string;
  groupName: string;
}

const Secrets: React.FC<ISecretsProps> = ({
  gitRootId,
  groupName,
}: ISecretsProps): JSX.Element => {
  const { t } = useTranslation();

  const defaultCurrentRow: ISecret = { description: "", key: "", value: "" };
  const [currentRow, updateRow] = useState(defaultCurrentRow);
  const [isUpdate, setIsUpdate] = useState(false);

  const [addSecretModalOpen, setAddSecretModalOpen] = useState(false);
  const { data, refetch } = useQuery<{ root: IGitRootAttr }>(GET_ROOT, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load secrets", error);
      });
    },
    variables: { groupName, rootId: gitRootId },
  });
  function editCurrentRow(
    key: string,
    value: string,
    description: string
  ): void {
    updateRow({ description, key, value });
    setIsUpdate(true);
    setAddSecretModalOpen(true);
  }

  const secretsDataSet =
    data === undefined
      ? []
      : data.root.secrets.map((item: ISecret): ISecretItem => {
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
  function closeModal(): void {
    setIsUpdate(false);
    updateRow(defaultCurrentRow);
    setAddSecretModalOpen(false);
  }
  function openModal(): void {
    setAddSecretModalOpen(true);
  }
  function isSecretDuplicated(key: string): boolean {
    return secretsDataSet.some((item): boolean => item.key === key);
  }

  return (
    <React.StrictMode>
      <Modal
        open={addSecretModalOpen}
        title={t("group.scope.git.repo.credentials.secrets.tittle")}
      >
        <AddSecret
          closeModal={closeModal}
          groupName={groupName}
          handleSubmitSecret={refetch}
          isDuplicated={isSecretDuplicated}
          isUpdate={isUpdate}
          rootId={gitRootId}
          secretDescription={currentRow.description}
          secretKey={currentRow.key}
          secretValue={currentRow.value}
        />
      </Modal>
      <Table
        dataset={secretsDataSet}
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
      <Button id={"add-secret"} onClick={openModal} variant={"secondary"}>
        {"Add secret"}
      </Button>
    </React.StrictMode>
  );
};

export { Secrets };
