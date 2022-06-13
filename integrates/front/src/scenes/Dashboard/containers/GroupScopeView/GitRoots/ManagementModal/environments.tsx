import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { AddEnvironment } from "./addEnvironment";

import type { IFormValues } from "../../types";
import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { Table } from "components/Table";

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

  function openAddModal(): void {
    setIsAddEnvModalOpen(true);
  }
  function closeAddModal(): void {
    setIsAddEnvModalOpen(false);
  }

  return (
    <React.Fragment>
      <Table
        dataset={initialValues.gitEnvironmentUrls}
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
