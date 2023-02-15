import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { ReportOptions } from "./ReportOptions";

import { Modal } from "components/Modal";
import { VerifyDialog } from "scenes/Dashboard/components/VerifyDialog";

interface IDeactivationModalProps {
  enableCerts: boolean;
  isOpen: boolean;
  typesOptions: string[];
  onClose: () => void;
  userRole: string;
}

const ReportsModal: React.FC<IDeactivationModalProps> = ({
  enableCerts,
  isOpen,
  typesOptions,
  onClose,
  userRole,
}: IDeactivationModalProps): JSX.Element => {
  const { t } = useTranslation();

  const [isFilterReportModalOpen, setIsFilterReportModalOpen] = useState(false);
  const [isVerifyDialogOpen, setIsVerifyDialogOpen] = useState(false);

  const closeFilterReportsModal: () => void = useCallback((): void => {
    setIsFilterReportModalOpen(false);
  }, []);
  const handleClose = useCallback((): void => {
    closeFilterReportsModal();
    onClose();
    setIsVerifyDialogOpen(false);
  }, [onClose, closeFilterReportsModal, setIsVerifyDialogOpen]);

  return (
    <React.StrictMode>
      <Modal
        onClose={handleClose}
        open={isOpen}
        title={t("group.findings.report.modalTitle")}
      >
        <VerifyDialog isOpen={isVerifyDialogOpen}>
          {(setVerifyCallbacks): JSX.Element => {
            return (
              <ReportOptions
                closeFilterReportsModal={closeFilterReportsModal}
                enableCerts={enableCerts}
                isFilterReportModalOpen={isFilterReportModalOpen}
                onClose={onClose}
                setIsFilterReportModalOpen={setIsFilterReportModalOpen}
                setIsVerifyDialogOpen={setIsVerifyDialogOpen}
                setVerifyCallbacks={setVerifyCallbacks}
                typesOptions={typesOptions}
                userRole={userRole}
              />
            );
          }}
        </VerifyDialog>
      </Modal>
    </React.StrictMode>
  );
};

export { ReportsModal };
