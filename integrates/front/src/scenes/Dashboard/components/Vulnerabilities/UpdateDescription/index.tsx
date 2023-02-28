import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";

import { ConfirmDialog } from "components/ConfirmDialog";
import { UpdateDescriptionContent } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/content";
import type { IUpdateDescriptionProps } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/types";

export const UpdateDescription: React.FC<IUpdateDescriptionProps> = ({
  changePermissions,
  findingId = "",
  isOpen = false,
  groupName,
  vulnerabilities,
  handleClearSelected,
  handleCloseModal,
  refetchData,
}: IUpdateDescriptionProps): JSX.Element => {
  const { t } = useTranslation();

  useEffect((): void => {
    if (isOpen && changePermissions !== undefined) {
      changePermissions(groupName as string);
    }
  }, [groupName, isOpen, changePermissions]);

  return (
    <React.StrictMode>
      <ConfirmDialog
        message={t("searchFindings.tabDescription.approvalMessage")}
        title={t("searchFindings.tabDescription.approvalTitle")}
      >
        {(confirm): JSX.Element => {
          return (
            <UpdateDescriptionContent
              confirm={confirm}
              findingId={findingId}
              groupName={groupName}
              handleClearSelected={handleClearSelected}
              handleCloseModal={handleCloseModal}
              refetchData={refetchData}
              vulnerabilities={vulnerabilities}
            />
          );
        }}
      </ConfirmDialog>
    </React.StrictMode>
  );
};
