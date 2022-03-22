import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";

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
          <ModalFooter>
            <Button onClick={onClick} variant={"primary"}>
              {t("registration.continueBtn")}
            </Button>
          </ModalFooter>
        </React.Fragment>
      </Modal>
    );
  };
