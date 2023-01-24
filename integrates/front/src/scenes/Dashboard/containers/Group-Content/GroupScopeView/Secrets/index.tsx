/* eslint-disable react/require-default-props */
import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { Row } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import { AddSecret } from "./addSecret";
import { renderSecretsDescription } from "./secretDescription";
import { SecretValue } from "./secretValue";

import { GET_ROOT } from "../queries";
import type { IGitRootAttr } from "../types";
import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { authzPermissionsContext } from "utils/authz/config";
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
  onCloseModal?: () => void;
}

const Secrets: React.FC<ISecretsProps> = ({
  gitRootId,
  groupName,
  onCloseModal = undefined,
}: ISecretsProps): JSX.Element => {
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canAddSecret: boolean = permissions.can(
    "api_mutations_add_secret_mutate"
  );

  const [modalMessages, setModalMessages] = useState({
    message: "",
    type: "success",
  });
  const [showAlert, setShowAlert] = useState(false);

  const defaultCurrentRow: ISecret = useMemo((): ISecret => {
    return { description: "", key: "", value: "" };
  }, []);
  const [currentRow, setCurrentRow] = useState(defaultCurrentRow);
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
  const editCurrentRow = useCallback(
    (key: string, value: string, description: string): void => {
      setShowAlert(false);
      setModalMessages({
        message: "",
        type: "success",
      });
      setCurrentRow({ description, key, value });
      setIsUpdate(true);
      setAddSecretModalOpen(true);
    },
    []
  );

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

  const closeModal = useCallback((): void => {
    setIsUpdate(false);
    setCurrentRow(defaultCurrentRow);
    setAddSecretModalOpen(false);
  }, [defaultCurrentRow]);

  const openModal = useCallback((): void => {
    setShowAlert(false);
    setModalMessages({
      message: "",
      type: "success",
    });
    setAddSecretModalOpen(true);
  }, []);

  function isSecretDuplicated(key: string): boolean {
    return secretsDataSet.some((item): boolean => item.key === key);
  }

  function handleRowExpand(row: Row<ISecretItem>): JSX.Element {
    return renderSecretsDescription({
      description: [row.original.description],
    });
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
          setModalMessages={setModalMessages}
        />
      </Modal>
      <Table
        columns={[
          {
            accessorKey: "key",
            header: String(t("group.scope.git.repo.credentials.secrets.key")),
          },
          {
            accessorKey: "element",
            cell: (cell: ICellHelper<ISecretItem>): JSX.Element =>
              cell.getValue(),
            header: String(t("group.scope.git.repo.credentials.secrets.value")),
          },
        ]}
        data={secretsDataSet}
        expandedRow={handleRowExpand}
        id={"tblGitRootSecrets"}
      />
      {!showAlert && modalMessages.message !== "" && (
        <Alert
          onTimeOut={setShowAlert}
          variant={modalMessages.type as IAlertProps["variant"]}
        >
          {modalMessages.message}
        </Alert>
      )}
      <Button
        disabled={!canAddSecret}
        id={"add-secret"}
        onClick={openModal}
        variant={"secondary"}
      >
        {"Add secret"}
      </Button>
      {_.isUndefined(onCloseModal) ? undefined : (
        <Button
          id={"git-root-add-secret-cancel"}
          onClick={onCloseModal}
          variant={"secondary"}
        >
          {t("components.modal.cancel")}
        </Button>
      )}
    </React.StrictMode>
  );
};

export { Secrets };
