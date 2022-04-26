import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React, { useCallback, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import { AddSecret } from "./addSecret";

import type { IEnvironmentUrl, ISecret } from "../../types";
import { renderSecretsDescription } from "../ManagementModal/secretDescription";
import { SecretValue } from "../ManagementModal/secretValue";
import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { Table } from "components/Table";
import { authzPermissionsContext } from "utils/authz/config";

interface ISecretItem {
  description: string;
  element: JSX.Element;
  key: string;
  value: string;
}

interface IManagementModalProps {
  closeModal: () => void;
  environmentUrl: IEnvironmentUrl;
  groupName: string;
  isOpen: boolean;
}
const ManagementEnvironmentUrlsModal: React.FC<IManagementModalProps> = ({
  groupName,
  isOpen,
  environmentUrl,
  closeModal,
}: IManagementModalProps): JSX.Element => {
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canAddSecret: boolean = permissions.can(
    "api_mutations_add_secret_mutate"
  );
  const defaultCurrentRow: ISecret = useMemo((): ISecret => {
    return { description: "", key: "", value: "" };
  }, []);
  const [currentRow, setCurrentRow] = useState(defaultCurrentRow);
  const [isUpdate, setIsUpdate] = useState(false);

  const [addSecretModalOpen, setAddSecretModalOpen] = useState(false);

  function editCurrentRow(
    key: string,
    value: string,
    description: string
  ): void {
    setCurrentRow({ description, key, value });
    setIsUpdate(true);
    setAddSecretModalOpen(true);
  }

  const secretsDataSet = environmentUrl.secrets.map(
    (item: ISecret): ISecretItem => {
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
    }
  );
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
            isDuplicated={isSecretDuplicated}
            isUpdate={isUpdate}
            secretDescription={currentRow.description}
            secretKey={currentRow.key}
            secretValue={currentRow.value}
            urlId={environmentUrl.id}
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
        <Button
          disabled={!canAddSecret}
          id={"add-secret"}
          onClick={openModal}
          variant={"secondary"}
        >
          {"Add secret"}
        </Button>
      </Modal>
    </React.StrictMode>
  );
};

export { ManagementEnvironmentUrlsModal };
