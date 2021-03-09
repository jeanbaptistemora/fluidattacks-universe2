import { Button } from "components/Button";
import { Modal } from "components/Modal";
import React from "react";
import { useTranslation } from "react-i18next";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";

interface IConcurrentSessionNoticeProps {
  open: boolean;
  onClick: () => void;
}

export const ConcurrentSessionNotice: React.FC<IConcurrentSessionNoticeProps> = (
  props: IConcurrentSessionNoticeProps
): JSX.Element => {
  const { open, onClick } = props;
  const { t } = useTranslation();

  return (
    <Modal headerTitle={t("registration.concurrentSessionTitle")} open={open}>
      <React.Fragment>
        <p>{t("registration.concurrentSessionMessage")}</p>
        <hr />
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button onClick={onClick}>{t("registration.continueBtn")}</Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      </React.Fragment>
    </Modal>
  );
};
