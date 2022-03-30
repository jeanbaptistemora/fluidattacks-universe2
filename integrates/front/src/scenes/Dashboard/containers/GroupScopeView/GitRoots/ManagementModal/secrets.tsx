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
  key: string;
  value: string;
}
interface ISecretItem {
  key: string;
  value: JSX.Element;
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
  const [addSecretModalOpen, setAddSecretModalOpen] = useState(false);

  const { data, refetch } = useQuery<{ root: IGitRootAttr }>(GET_ROOT, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load secrets", error);
      });
    },
    variables: { groupName, rootId: gitRootId },
  });

  const secretsDataSet =
    data === undefined
      ? []
      : data.root.secrets.map((item: ISecret): ISecretItem => {
          return {
            key: item.key,
            value: <SecretValue value={item.value} />,
          };
        });
  function closeModal(): void {
    setAddSecretModalOpen(false);
  }
  function openModal(): void {
    setAddSecretModalOpen(true);
  }
  function isSecretDuplicated(key: string): boolean {
    return secretsDataSet.some((item): boolean => item.key === key);
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
          handleSubmitSecret={refetch}
          isDuplicated={isSecretDuplicated}
          key={""}
          rootId={gitRootId}
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
