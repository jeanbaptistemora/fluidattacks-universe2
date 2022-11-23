import React from "react";
import { useTranslation } from "react-i18next";

import { Modal, ModalConfirm } from "components/Modal";

interface IConcurrentSessionNoticeProps {
  open: boolean;
  onClick: () => void;
}

export const ConcurrentSessionNotice: React.FC<IConcurrentSessionNoticeProps> =
  (props: IConcurrentSessionNoticeProps): JSX.Element => {
    const { open, onClick } = props;
    const { t } = useTranslation();

    return (
      <Modal open={open} title={t("registration.concurrentSessionTitle")}>
        <React.Fragment>
          <p>{t("registration.concurrentSessionMessage")}</p>
          <ModalConfirm
            onConfirm={onClick}
            txtConfirm={t("registration.continue")}
          />
        </React.Fragment>
      </Modal>
    );
  };
