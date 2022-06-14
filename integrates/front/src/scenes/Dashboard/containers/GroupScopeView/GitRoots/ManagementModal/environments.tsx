import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { AddEnvironment } from "./addEnvironment";

import { GET_ROOT_ENVIRONMENT_URLS } from "../../queries";
import type { IFormValues, IGitRootAttr } from "../../types";
import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { Table } from "components/Table";
import { Logger } from "utils/logger";

interface IEnvironmentsProps {
  rootInitialValues: IFormValues;
  groupName: string;
  onClose: () => void;
}

const Environments: React.FC<IEnvironmentsProps> = ({
  rootInitialValues,
  groupName,
  onClose,
}: IEnvironmentsProps): JSX.Element => {
  const { t } = useTranslation();

  const [isAddEnvModalOpen, setIsAddEnvModalOpen] = useState(false);
  const initialValues = { ...rootInitialValues, other: "", reason: "" };
  const { data, refetch } = useQuery<{ root: IGitRootAttr }>(
    GET_ROOT_ENVIRONMENT_URLS,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load secrets", error);
        });
      },
      variables: { groupName, rootId: initialValues.id },
    }
  );

  function openAddModal(): void {
    setIsAddEnvModalOpen(true);
  }
  function closeAddModal(): void {
    setIsAddEnvModalOpen(false);
  }

  return (
    <React.Fragment>
      <Table
        dataset={
          _.isUndefined(data) || _.isNull(data)
            ? []
            : data.root.gitEnvironmentUrls
        }
        exportCsv={false}
        headers={[
          {
            dataField: "url",
            header: t("group.scope.git.envUrl"),
          },
          {
            dataField: "urlType",
            header: t("group.scope.git.envUrlType"),
          },
        ]}
        id={"tblGitRootSecrets"}
        pageSize={10}
        search={false}
      />

      <Modal
        onClose={closeAddModal}
        open={isAddEnvModalOpen}
        title={t("group.scope.git.addEnvUrl")}
      >
        <AddEnvironment
          closeFunction={closeAddModal}
          groupName={groupName}
          onSubmit={refetch}
          rootId={initialValues.id}
        />
      </Modal>
      <ModalFooter>
        <Button onClick={onClose} variant={"secondary"}>
          {t("confirmmodal.cancel")}
        </Button>
        <Button id={"add-env-url"} onClick={openAddModal} variant={"primary"}>
          {t("group.scope.git.addEnvUrl")}
        </Button>
      </ModalFooter>
    </React.Fragment>
  );
};

export { Environments };
