import React from "react";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route } from "react-router-dom";

import { Repository } from "./repository";

import type { IGitRootAttr } from "../../types";
import { Modal } from "components/Modal";

interface IManagementModalProps {
  initialValues: IGitRootAttr | undefined;
  nicknames: string[];
  onClose: () => void;
  onSubmitRepo: (values: IGitRootAttr) => Promise<void>;
}

const ManagementModal: React.FC<IManagementModalProps> = ({
  initialValues,
  nicknames,
  onClose,
  onSubmitRepo,
}: IManagementModalProps): JSX.Element => {
  const { t } = useTranslation();
  const isEditing: boolean = initialValues !== undefined;

  return (
    <Modal
      headerTitle={t(`group.scope.common.${isEditing ? "edit" : "add"}`)}
      open={true}
    >
      <MemoryRouter initialEntries={["/repository"]}>
        <Route path={"/repository"}>
          <Repository
            initialValues={initialValues}
            isEditing={isEditing}
            nicknames={nicknames}
            onClose={onClose}
            onSubmit={onSubmitRepo}
          />
        </Route>
      </MemoryRouter>
    </Modal>
  );
};

export { ManagementModal };
