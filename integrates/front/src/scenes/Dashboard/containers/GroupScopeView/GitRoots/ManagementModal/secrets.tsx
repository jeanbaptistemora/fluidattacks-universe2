import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { AddSecret } from "./addSecret";
import { SecretValue } from "./secretValue";

import type { IGitRootAttr } from "../../types";
import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { Table } from "components/Table";

interface ISecret {
  key: string;
  value: string;
}
interface ISecretItem {
  key: string;
  value: JSX.Element;
}

interface ISecretsProps {
  initialValues: IGitRootAttr;
  groupName: string;
}

const Secrets: React.FC<ISecretsProps> = ({
  initialValues,
  groupName,
}: ISecretsProps): JSX.Element => {
  const { t } = useTranslation();
  const [addSecretModalOpen, setAddSecretModalOpen] = useState(false);
  const secretsDataSet = initialValues.secrets.map(
    (item: ISecret): ISecretItem => {
      return {
        key: item.key,
        value: <SecretValue value={item.value} />,
      };
    }
  );
  function closeModal(): void {
    setAddSecretModalOpen(false);
  }
  function openModal(): void {
    setAddSecretModalOpen(true);
  }

  return (
    <div>
      <Modal
        open={addSecretModalOpen}
        title={t("group.scope.git.repo.credentials.secrets.tittle")}
      >
        <AddSecret
          closeModal={closeModal}
          groupName={groupName}
          key={""}
          rootId={initialValues.id}
          value={""}
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
            dataField: "value",
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
    </div>
  );
};

export { Secrets };
